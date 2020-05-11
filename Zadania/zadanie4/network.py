import socket
import pickle


class Network:
    def __init__(self, server_address):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_address
        self.port = 7777
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_init_data(self):
        return self.p

    def connect(self):
        try:
            print("Trying to connect with " + self.server + "...")
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            print("Cannot connect")
            exit()

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def receive(self):
        return pickle.loads(self.client.recv(2048))

    def disconnect(self):
        self.client.close()