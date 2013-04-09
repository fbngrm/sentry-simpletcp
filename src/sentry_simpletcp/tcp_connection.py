import socket

class TCPConnection(object):
    def __init__(self):
        self.socket = None

    def connect(self, host='127.0.0.1', port=8123):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send(self, data):
        if not self.socket:
            self.connect()
        self.socket.send(data + '\r\n')
        #time.sleep(0.05)

    def close(self):
        self.socket.close()
        