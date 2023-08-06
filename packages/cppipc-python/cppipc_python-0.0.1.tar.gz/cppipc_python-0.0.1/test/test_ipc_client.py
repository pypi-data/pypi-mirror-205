from cppipc_python import Dog, ShareMemClient, ShareMemServer
import time, threading, atexit

client = ShareMemClient("qq3", True)

def client_fn(client):
    while True:
        # time.sleep(10)
        rep = client.send_and_wait_reply("np.array([1,2,3])")


thread_hello = threading.Thread(target=client_fn, args=(client,))
print('thread_hello.start()')
thread_hello.start()

try:
    while True:
        time.sleep(0.2)
        print('k')
except:
    print('int')
    # thread_hello.join()
    # client.disconnect()

# python test/test_ipc_client.py