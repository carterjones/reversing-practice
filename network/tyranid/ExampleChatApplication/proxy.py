import importlib
import socket
from threading import Thread

import click

import parser


def log(src, msg):
    prefix = f"[{src}]"
    print(f"{prefix:<8} {msg}")


class Proxy2Server(Thread):
    def __init__(self, host, port) -> None:
        super(Proxy2Server, self).__init__()
        self.host = host
        self.port = port
        self.client_socket = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def log(self, msg):
        log("server", msg)

    def run(self):
        self.server_socket.connect((self.host, self.port))
        old_data = None
        while True:
            new_data = self.server_socket.recv(4096)
            if new_data:
                data = new_data
                importlib.reload(parser)
                try:
                    if old_data:
                        data = old_data + data
                    packet = parser.parse(data, "server")
                    self.log("pkt: " + str(packet))
                    old_data = None
                except Exception:
                    # old_data is used to account for situations where the TCP
                    # stream does not send all the data at once, but instead
                    # splits it across TCP packets. This error handling is
                    # nowhere near sufficient for all cases, but it works well
                    # enough for the purpose of this project.
                    old_data = data
                self.client_socket.sendall(new_data)


class Client2Proxy(Thread):
    def __init__(self, host, port) -> None:
        super(Client2Proxy, self).__init__()
        self.host = host
        self.port = port
        self.server_socket = None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(1)
            self.client_socket, addr = s.accept()

    def log(self, msg):
        log("client", msg)

    def run(self):
        old_data = None
        while True:
            new_data = self.client_socket.recv(4096)
            if new_data:
                data = new_data
                importlib.reload(parser)
                try:
                    if old_data:
                        data = old_data + data
                    packet = parser.parse(data, "client")
                    self.log("pkt: " + str(packet))
                    old_data = None
                except Exception:
                    # old_data is used to account for situations where the TCP
                    # stream does not send all the data at once, but instead
                    # splits it across TCP packets. This error handling is
                    # nowhere near sufficient for all cases, but it works well
                    # enough for the purpose of this project.
                    old_data = data
                self.server_socket.sendall(new_data)


class Proxy(Thread):
    def __init__(self, from_host, from_port, to_host, to_port) -> None:
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.from_port = from_port
        self.to_host = to_host
        self.to_port = to_port

    def log(self, msg):
        log("proxy", msg)

    def run(self):
        self.log(f"listening on  {self.from_host}:{self.from_port}")
        self.log(f"forwarding to {self.to_host}:{self.to_port}")
        ctr = 0
        while True:
            self.log(f"{ctr}: setting up")
            self.c2p = Client2Proxy(self.from_host, self.from_port)
            self.p2s = Proxy2Server(self.to_host, self.to_port)
            self.log(f"{ctr}: connection established")
            self.c2p.server_socket = self.p2s.server_socket
            self.p2s.client_socket = self.c2p.client_socket
            self.c2p.start()
            self.p2s.start()
            ctr += 1


@click.command()
@click.argument('from_host', default='0.0.0.0')
@click.argument('from_port', default=3333)
@click.argument('to_host', default='127.0.0.1')
@click.argument('to_port', default=12345)
def click_main(from_host, from_port, to_host, to_port):
    main_server = Proxy(from_host, from_port, to_host, to_port)
    main_server.start()


if __name__ == "__main__":
    click_main()
