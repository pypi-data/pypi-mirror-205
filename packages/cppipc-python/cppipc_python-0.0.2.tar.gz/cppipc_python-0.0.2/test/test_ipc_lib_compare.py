import os, pickle, atexit
from cppipc_python import py_channel
import socket, threading, pickle, uuid, os, atexit, time, json, psutil

BUFSIZE = 10485760
DEBUG_NETWORK = False
class StreamingPackageSep:
    def __init__(self):
        self.buff = [b'']
        self.myEOF = b'\xaa\x55\xaaHMP\xaa\x55'    # those bytes follow 010101 or 101010 pattern
        # self.myEOF = b'#A5@5A#'    # the EOF string for frame seperation

    def lower_send(self, data, connection):
        if DEBUG_NETWORK: assert self.myEOF not in data, 'This is (almost) not possible!'
        data = data + self.myEOF
        if DEBUG_NETWORK: print('data length:', len(data))
        connection.send(data)

    def lowest_recv(self, connection):
        while True:
            recvData = connection.recv(BUFSIZE)
            # ends_with_mark = recvData.endswith(self.myEOF)
            split_res = recvData.split(self.myEOF)
            assert len(split_res) != 0
            if len(split_res) == 1:
                # 说明没有终止符，直接将结果贴到buf最后一项
                self.buff[-1] = self.buff[-1] + split_res[0]
                if self.myEOF in self.buff[-1]: self.handle_flag_breakdown()
            else:
                n_split = len(split_res)
                for i, r in enumerate(split_res):
                    self.buff[-1] = self.buff[-1] + r   # 追加buff
                    if i == 0 and (self.myEOF in self.buff[-1]): 
                        # 第一次追加后，在修复的数据断面上发现了myEOF！
                        self.handle_flag_breakdown()
                    if i != n_split-1: 
                        # starts a new entry
                        self.buff.append(b'')
                    else:  
                        # i == n_split-1, which is the last item
                        if r == b'': continue
            if len(self.buff)>=2:
                # 数据成型，拿取成型的数据
                buff_list = self.buff[:-1]  
                self.buff = self.buff[-1:]
                return buff_list

    # Fox-Protocal
    def lower_recv(self, connection, expect_single=True):
        buff_list = self.lowest_recv(connection)
        if expect_single:
            assert len(buff_list) == 1, ('一次拿到了多帧数据, 但expect_single=True, 触发错误.', buff_list)
            return buff_list[0], connection
        else:
            return buff_list, connection


    def handle_flag_breakdown(self):
        split_ = self.buff[-1].split(self.myEOF)
        assert len(split_)==2
        self.buff[-1] = split_[0]
        # starts a new entry
        self.buff.append(b'')
        self.buff[-1] = split_[1]
        return

class UnixTcpServerP2P(StreamingPackageSep):
    def __init__(self, unix_path, obj='bytes') -> None:
        super().__init__()
        try: os.makedirs(os.path.dirname(unix_path))
        except: pass
        self.unix_path = unix_path
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(self.unix_path)
        self.server.listen()
        self.most_recent_client = None
        self.use_pickle = (obj=='pickle')
        self.convert_str = (obj=='str')
        atexit.register(self.__del__)

    def accept_conn(self):
        conn, _  = self.server.accept()
        return conn

    def wait_next_dgram(self):
        if self.most_recent_client is None: self.most_recent_client, _ = self.server.accept()
        data, self.most_recent_client = self.lower_recv(self.most_recent_client)
        if DEBUG_NETWORK: print('self.most_recent_client',self.most_recent_client)
        if self.convert_str: data = data.decode('utf8')
        if self.use_pickle: data = pickle.loads(data)
        if DEBUG_NETWORK: print('recv from :', self.most_recent_client, ' data :', data)
        return data

    def reply_last_client(self, data):
        assert self.most_recent_client is not None
        if DEBUG_NETWORK: print('reply_last_client :', self.most_recent_client, ' data :', data)
        if self.use_pickle: data = pickle.dumps(data)
        if self.convert_str: data = bytes(data, encoding='utf8')
        self.lower_send(data, self.most_recent_client)
        return

    def __del__(self):
        self.server.close()
        try: os.remove(self.unix_path)
        except: pass
        return


class UnixTcpClientP2P(StreamingPackageSep):
    def __init__(self, target_unix_path, self_unix_path=None, obj='bytes') -> None:
        super().__init__()
        self.target_unix_path = target_unix_path
        if self_unix_path is not None:
            self.self_unix_path = self_unix_path  
        else:
            self.self_unix_path = target_unix_path+'_client_'+uuid.uuid1().hex[:5]
        self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.client.bind(self.self_unix_path)
        self.use_pickle = (obj=='pickle')
        self.convert_str = (obj=='str')
        self.connected = False
        atexit.register(self.__del__)

    def send_dgram_to_target(self, data):
        if self.use_pickle: data = pickle.dumps(data)
        if self.convert_str: data = bytes(data, encoding='utf8')
        if not self.connected: self.client.connect(self.target_unix_path); self.connected = True
        self.lower_send(data, self.client)
        if DEBUG_NETWORK: print('send_targeted_dgram :', self.client, ' data :', data)
        return

    def send_and_wait_reply(self, data):
        if self.use_pickle: data = pickle.dumps(data)
        if self.convert_str: data = bytes(data, encoding='utf8')
        if not self.connected: self.client.connect(self.target_unix_path); self.connected = True
        self.lower_send(data, self.client)
        data, _ = self.lower_recv(self.client)
        if self.convert_str: data = data.decode('utf8')
        if self.use_pickle: data = pickle.loads(data)
        if DEBUG_NETWORK: print('get_reply :', self.client, ' data :', data)
        return data

    def __del__(self):
        self.client.close()
        os.remove(self.self_unix_path)
        return



class ShmP2PServer:
    def __init__(self, unix_path, obj='bytes') -> None:
        self.server = py_channel("test_channel_server", "receiver")
        self.client = py_channel("test_channel_client", "sender")
        self.use_pickle = (obj=='pickle')
        self.convert_str = (obj=='str')

    def close_shm(self):
        try:
            self.client.py_close()
            self.server.py_close()
        except:
            pass

    def lower_recv(self):
        while True:
            res = self.server.py_recv(300)    # 等待300ms
            if (res is not None) and len(res) != 0:
                return res
            if DEBUG_NETWORK: print('Get Nothing')

    def lower_send(self, data):
        self.client.py_send(data, 500)

    def wait_next_dgram(self):
        data = self.lower_recv()
        if self.convert_str: data = data.decode('utf8')
        if self.use_pickle: data = pickle.loads(data)
        if DEBUG_NETWORK: print('data :', data)
        return data

    def reply_last_client(self, data):
        if DEBUG_NETWORK: print('reply data :', data)
        if self.use_pickle: data = pickle.dumps(data)
        if self.convert_str: data = bytes(data, encoding='utf8')
        self.lower_send(data)
        return
    
    def __del__(self):
        self.close_shm()
        return
    
class ShmP2PClient:
    def __init__(self, target_unix_path, self_unix_path=None, obj='bytes') -> None:
        self.client = py_channel("test_channel_client", "receiver")
        self.server = py_channel("test_channel_server", "sender")
        self.use_pickle = (obj=='pickle')
        self.convert_str = (obj=='str')

    def close_shm(self):
        try:
            self.client.py_close()
            self.server.py_close()
            print('closed')
        except:
            pass

    def lower_recv(self):
        while True:
            res = self.client.py_recv(300)    # 等待300ms
            if (res is not None) and len(res) != 0:
                return res
            if DEBUG_NETWORK: print('Get Nothing')

    def lower_send(self, data):
        # print('send', data)
        self.server.py_send(data, 500)

    def send_dgram_to_target(self, data):
        if self.use_pickle: data = pickle.dumps(data)
        if self.convert_str: data = bytes(data, encoding='utf8')
        self.lower_send(data)
        if DEBUG_NETWORK: print('send data :', data)
        return

    def send_and_wait_reply(self, data):
        if self.use_pickle: data = pickle.dumps(data)
        if self.convert_str: data = bytes(data, encoding='utf8')
        self.lower_send(data)
        data = self.lower_recv()
        if self.convert_str: data = data.decode('utf8')
        if self.use_pickle: data = pickle.loads(data)
        if DEBUG_NETWORK: print('get reply data :', data)
        return data
    
    def __del__(self):
        self.close_shm()
        return
    
import time
import threading, uuid
import numpy as np
remote_uuid = uuid.uuid1().hex   # use uuid to identify threads

unix_path = 'TEMP/Sockets/unix/%s'%remote_uuid
server = UnixTcpServerP2P(unix_path, obj='pickle')
client = UnixTcpClientP2P(unix_path, obj='pickle')

def server_fn():
    cnt = 0
    while True:
        data = server.wait_next_dgram()
        time.sleep(1)
        server.reply_last_client(np.array([cnt, 4,5,6]))
        cnt += 1

def client_fn():
    cnt = 0
    while True:
        tic = time.time()
        rep = client.send_and_wait_reply(np.ones(shape=(1000,10000)))
        toc = time.time()
        print(toc-tic, rep)
        cnt += 1


thread_hi = threading.Thread(target=server_fn)
thread_hello = threading.Thread(target=client_fn)
# 启动线程
thread_hi.start()
thread_hello.start()


