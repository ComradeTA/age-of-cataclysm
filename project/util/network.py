import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = "127.0.0.1"
        self.port = 28420
        self.addr = (self.server, self.port)


    def connect(self, client_id, data):
        try:
            print("Connecting to:", self.addr)
            self.client.sendto(pickle.dumps(data), self.addr)
            print("Waiting...")
            ''
            self.client.settimeout(10)
            
            try:
                data, addr = self.client.recvfrom(2048)
            except Exception as e:
                print("Failed to connect:", e)
                return
            p = pickle.loads(data)
            print("Connected.")
            print(p)
            self.client.settimeout(None)
            return p
        except Exception as e:
            print(e)
            pass

    def send(self, data):
        try:
            self.client.sendto(pickle.dumps(data), self.addr)
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            data, addr = self.client.recvfrom(2048)
        except Exception as e:
            print("Failed to receive:", e)
            return
        return pickle.loads(data)

