import socket
import threading


class MockSockContext(threading.Thread):
    """MockSock context manager mocks 3rd party APIs.
     It works similar to real HTTP server in localhost environment.
     It is good for testing API that relies on 3rd party API calls.

     MockSock input parameter and return are the same: raw HTTP response
     string, that can be prepared by according to one's testing needs.
    """
    def __init__(self, response, port=80, host='localhost'):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.response = response
        self.buffer_size = 4096
        self.mock_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mock_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, *args):
        self.mock_sock.close()

    def start_sock(self):
        try:
            self.mock_sock.bind((self.host, self.port))
        except socket.error:
            print(socket.error)

        self.mock_sock.listen(0)
        conn, addr = self.mock_sock.accept()
        conn.recv(self.buffer_size)
        with conn:
            conn.sendall(self.response)

    def run(self):
        threading.Thread(name='start_sock', target=self.start_sock).start()
