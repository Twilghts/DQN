import socket
import threading
import time


def server_thread():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12340))
    server.listen()
    conn, addr = server.accept()
    conn.settimeout(5)  # Set timeout for 5 sec
    try:
        data = conn.recv(1024)
        if data:
            # conn.send(transfer_package)
            print(f"收到来自{addr}的消息")
    except socket.timeout:
        print("Timeout occurred, continue running")

    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    server.close()


# print("server准备关闭了！")


def client_thread():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    try:
        client.connect(('127.0.0.1', 12340))
        client.send(bytes("你好", encoding='utf-8'))
        # transfer_package = client.recv(1024)
        # print(str(transfer_package, encoding='utf-8'))
    except socket.timeout:
        print("Timeout occurred, continue running")
    except socket.error as e:
        print("Socket error: ", e)
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    # print("client准备关闭了！")


if __name__ == '__main__':
    start_time = time.perf_counter()
    running = True
    # server_thread = threading.Thread(_target=server_thread)
    # client_thread = threading.Thread(_target=client_thread)
    # server_thread._start()
    # client_thread._start()
    count = 1
    for i in range(100):
        print(f"第{count}次发送消息")
        Server_thread = threading.Thread(target=server_thread)
        Client_thread = threading.Thread(target=client_thread)
        Server_thread.start()
        Client_thread.start()
        Server_thread.join()
        Client_thread.join()
        count += 1
        if not Client_thread.is_alive() and Server_thread.is_alive():
            continue
    # try:
    #     while True:
    #         pass
    #     print('运行得到这里来吗？')
    # except KeyboardInterrupt:
    #     running = False
    #     server_thread.join()
    #     client_thread.join()
    print(f"消耗时间: {time.perf_counter() - start_time}")
