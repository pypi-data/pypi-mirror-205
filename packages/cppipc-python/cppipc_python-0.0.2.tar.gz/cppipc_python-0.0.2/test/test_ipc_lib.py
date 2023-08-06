import os, pickle, atexit
from cppipc_python import py_channel
import socket, threading, pickle, uuid, os, atexit, time, json, psutil

BUFSIZE = 10485760
DEBUG_NETWORK = False


class UnixUdpServer:
    def __init__(self, unix_path, obj='bytes') -> None:
        try: os.makedirs(os.path.dirname(unix_path))
        except: pass
        self.unix_path = unix_path
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server.bind(self.unix_path)
        self.most_recent_client = None
        self.use_pickle = (obj=='pickle')
        self.convert_str = (obj=='str')
        return

    def wait_next_dgram(self):
        data, self.most_recent_client = self.server.recvfrom(BUFSIZE)
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
        self.server.sendto(data, self.most_recent_client)
        return

    def __del__(self):
        self.server.close()
        os.unlink(self.unix_path)
        return

class UnixUdpTargetedClient:
    def __init__(self, target_unix_path, self_unix_path=None, obj='bytes') -> None:
        self.target_unix_path = target_unix_path
        if self_unix_path is not None:
            self.self_unix_path = self_unix_path  
        else:
            self.self_unix_path = target_unix_path+'_client_'+uuid.uuid1().hex[:5]
        self.client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.client.bind(self.self_unix_path)
        self.use_pickle = (obj=='pickle')
        self.convert_str = (obj=='str')
        return

    def send_dgram_to_target(self, data):
        if self.use_pickle: data = pickle.dumps(data)
        if self.convert_str: data = bytes(data, encoding='utf8')
        self.client.sendto(data, self.target_unix_path)
        if DEBUG_NETWORK: print('send_targeted_dgram :', self.target_unix_path, ' data :', data)
        return

    def send_and_wait_reply(self, data):
        if self.use_pickle: data = pickle.dumps(data)
        if self.convert_str: data = bytes(data, encoding='utf8')
        self.client.sendto(data, self.target_unix_path)
        data, _ = self.client.recvfrom(BUFSIZE)
        if self.convert_str: data = data.decode('utf8')
        if self.use_pickle: data = pickle.loads(data)
        if DEBUG_NETWORK: print('get_reply :', self.target_unix_path, ' data :', data)
        return data
    
    def __del__(self):
        self.client.close()
        os.unlink(self.self_unix_path)
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
server = ShmP2PServer(unix_path, obj='pickle')
client = ShmP2PClient(unix_path, obj='pickle')

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


