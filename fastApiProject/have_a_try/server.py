import socket
import selectors
import threading
import time


class SocketServer:
    seq = selectors.DefaultSelector()

    def __int__(self, host, port):
        self.host = host
        self.port = port
        self.clients = list()
        self._running = True

    def build(self, message):
        data = bytearray(message, 'ascii')
        length = len(data) + 2
        m = bytes([length >> 8, length & 0xff
                   ]) + bytes.fromhex('1f 41') + data + bytes.fromhex('ff')
        return m

    def start(self):
        t1 = threading.Thread(target=self.thread_main)
        t1.daemon = True
        t1.start()

        t2 = threading.Thread(target=self.send)
        t2.daemon = True
        t2.start()

    def thread_main(self):
        try:
            sock = socket.socket()
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen(10)
            sock.setblocking(False)
            self.seq.register(sock, selectors.EVENT_READ, self.accept)

            while self._running:
                events = self.seq.select(timeout=2)
                for key, mask in events:
                    callback = key.data
                    try:
                        callback(key.fileobj, mask)
                    except sock.error as e:
                        print(e)
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.seq.register(conn, selectors.EVENT_READ, self.read)
        try:
            conn.send("This is a begin task!!!")
            self.clients.append(conn)
            self.send_init_conn(conn)
        except Exception as e:
            self.seq.unregister(conn)
            conn.close()
            print(e)

    def read(self, conn, mask):
        try:
            data = conn.recv(1024)
        except Exception as e:
            self.seq.unregister(conn)
        time.sleep(1)

    def send(self):
        while True:
            for conn in self.clients:
                try:
                    conn.send("This is a test!!!")
                except Exception as e:
                    self.seq.unregister(conn)
                    conn.close()
                    self.clients.remove(conn)
                    print(e)
            time.sleep(10)

    def send_task(self, sender, task):
        for i, conn in enumerate(self.clients):
            try:
                conn.send(task)
            except Exception as e:
                print(e)

    def send_init_conn(self, conn):
        try:
            conn.send("This is a init task!!!")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    server = SocketServer('127.0.0.1', 8081)
    server.start()

    while True:
        time.sleep(10)
