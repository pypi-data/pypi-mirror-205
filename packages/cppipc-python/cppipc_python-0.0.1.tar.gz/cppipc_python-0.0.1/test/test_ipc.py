from cppipc_python import py_channel
import time, threading

sender = py_channel("test_channel2", "sender")
receiver = py_channel("test_channel2", "receiver")
sender.py_send(b"I'm Alice. Hello Bob. This a shm com!", 50)
# sender.send(sender)
result = receiver.py_recv(12)
print(result)
print('Bob hear:', result)

sender2 = py_channel("test_channel3", "sender")
receiver2 = py_channel("test_channel3", "receiver")
sender2.py_send(b"I'm BoB. Hello Alice. Shm com received!", 50)
# sender.send(sender)
result2 = receiver2.py_recv(12)
print(result2)
print('Bob hear:', result2)


# server = ShareMemServer("qq", True)
# client = ShareMemClient("qq", True)


# # import numpy as np

# # server = UdpServer(ip_port, obj='pickle')
# # client = UdpTargetedClient(ip_port, obj='pickle')

# def server_fn():
#     cnt = 0
#     while True:
#         data = server.wait_next_dgram()
#         server.reply(f"np.array --- {cnt}")
#         cnt += 1

# def client_fn():
#     while True:
#         rep = client.send_and_wait_reply("np.array([1,2,3])")


# thread_hi = threading.Thread(target=server_fn)
# thread_hello = threading.Thread(target=client_fn)
# # 启动线程
# print('thread_hi.start()')
# thread_hi.start()

# print('thread_hello.start()')
# thread_hello.start()
# # python test/test_ipc.py 
input('')