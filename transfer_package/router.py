import socket

from create_file import data_by_one_time

_ip = '127.0.0.1'
_ports = [n for n in range(20000, 20100)]


# print(_ports)
class Router:
    def __init__(self, number: int):
        self._ip = _ip
        self._port = _ports[number]
        self._message = None

    def server_thread(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self._ip, self._port))
        server.listen()
        conn, addr = server.accept()
        conn.settimeout(5)  # Set timeout for 5 sec

        try:
            # Receive transfer_package from the server
            data = b''
            while True:
                chunk = conn.recv(int(data_by_one_time))
                if chunk:
                    data += chunk
                else:
                    break
            if data:
                # conn.send(transfer_package)
                print(f"路由器{(self._ip, self._port)}收到来自{addr}的消息")
                self._message = data
        except socket.timeout:
            print("Timeout occurred, continue running")

        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        server.close()

    def client_thread(self, port: int):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        try:
            client.connect((_ip, port))
            client.send(self._message)
            # transfer_package = client.recv(1024)
            # print(transfer_package)
        except socket.timeout:
            print("Timeout occurred, continue running")
        except socket.error as e:
            print("Socket error: ", e)
        client.shutdown(socket.SHUT_RDWR)
        client.close()

    def save(self, message):
        self._message = bytes(message, encoding='utf-8')

    def show(self):
        if self._message:
            print(str(self._message, encoding='utf-8'))

    def get_port(self):
        return self._port

    def get_ip(self):
        return self._ip

    def get_message(self):
        return self._message
