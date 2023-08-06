from cppipc_python import Dog, ShareMemClient, ShareMemServer
import time, threading

server = ShareMemServer("qq3", True)


# def server_fn():
cnt = 0
while True:
    data = server.wait_next_dgram()
    server.reply(f"np.array --- {cnt}")
    cnt += 1


# thread_hi = threading.Thread(target=server_fn)
# print('thread_hi.start()')
# thread_hi.start()
try:
    while True:
        time.sleep(0.2)
        print('k')
except:
    print('int')
    server.disconnect()

# python test/test_ipc_server.py
