import socket


def server_thread(ip: str, port: int, message):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12340))
    server.listen()
    conn, addr = server.accept()
    conn.settimeout(5)  # Set timeout for 5 sec

    try:
        data = conn.recv(1024)
        if data:
            conn.send(data)
    except socket.timeout:
        print("Timeout occurred, continue running")

    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    server.close()


def client_thread():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    try:
        client.connect(('127.0.0.1', 12340))
        client.send(b'Hello, World!')
        data = client.recv(1024)
        print(data)
    except socket.timeout:
        print("Timeout occurred, continue running")
    except socket.error as e:
        print("Socket error: ", e)
    client.shutdown(socket.SHUT_RDWR)
    client.close()
