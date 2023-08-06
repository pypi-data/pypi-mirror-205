import os, pickle
from cppipc_python import py_channel

DEBUG_NETWORK = False
class ShmP2PServer:
    def __init__(self, unix_path, obj='bytes') -> None:
        self.server = py_channel("test_channel_server", "receiver")
        self.client = py_channel("test_channel_client", "sender")
        self.use_pickle = (obj=='pickle')
        self.convert_str = (obj=='str')
        return

    def lower_recv(self):
        while True:
            res = self.server.py_recv(300)    # 等待300ms
            if (res is not None) and len(res) != 0:
                if DEBUG_NETWORK: print('Get ', res)
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
        self.client.py_close()
        self.server.py_close()
        return

class ShmP2PClient:
    def __init__(self, target_unix_path, self_unix_path=None, obj='bytes') -> None:
        self.client = py_channel("test_channel_client", "receiver")
        self.server = py_channel("test_channel_server", "sender")
        self.use_pickle = (obj=='pickle')
        self.convert_str = (obj=='str')
        return
    
    def lower_recv(self):
        while True:
            res = self.client.py_recv(300)    # 等待300ms
            if (res is not None) and len(res) != 0:
                # if DEBUG_NETWORK: print('Get ', res)
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
        self.client.py_close()
        self.server.py_close()
        return
    
import time
import threading, uuid
import numpy as np
remote_uuid = uuid.uuid1().hex   # use uuid to identify threads

unix_path = 'TEMP/Sockets/unix/%s'%remote_uuid
server = ShmP2PServer(unix_path, obj='pickle')
client = ShmP2PClient(unix_path, obj='pickle')

def server_fn():
    while True:
        data = server.wait_next_dgram()
        time.sleep(1)
        server.reply_last_client(np.array([4,5,6]))


thread_hi = threading.Thread(target=server_fn, daemon=True)
# 启动线程
thread_hi.start()
input()