import multiprocessing
import socket


def server_process():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 1234))
    server.listen()
    conn, addr = server.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.send(data)
    conn.close()


def client_process():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 1234))
    client.send(b'Hello, World!')
    data = client.recv(1024)
    print(data)
    client.close()


if __name__ == '__main__':
    server = multiprocessing.Process(target=server_process)
    client = multiprocessing.Process(target=client_process)
    server.start()
    client.start()
    server.join()
    client.join()
