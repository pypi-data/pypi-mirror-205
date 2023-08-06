import socket
import threading
import time
from stats import Stats

class Tello:

    def __init__(self, tello_ip: str):
        self.local_ip = '127.0.0.1'
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.local_ip, self.local_port))

        self.receive_thread = threading.Thread(target=self.receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_ip = tello_ip
        self.tello_port = 8889
        self.tello_address = (self.tello_ip, self.tello_port)
        self.log = []

        self.MAX_TIME_OUT = 5.0

        self.send_command("command")


    def send_command(self, command):
        self.log.append(Stats(command, len(self.log)))

        self.socket.sendto(command.encode('utf-8'), self.tello_address)
        print('Sending command {0} to {1}'.format(command, self.tello_ip))

        start = time.time()
        while not self.log[-1].got_response():
            now = time.time()
            diff = now - start
            if diff > self.MAX_TIME_OUT:
                print ('Max timeout reached')
                return
        print('Command received by {0}'.format(self.tello_address))


    def receive_thread(self):
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                print('received {0} from {1}'.format(self.response, ip))

                self.log[-1].add_response(self.response)
            except socket.error as exc:
                print('Exception in socket: {0}'.format(exc))


    def on_close(self):
        for ip in self.tello_ip_list:
            self.socket.sendto('land'.encode('utf-8'), (ip, 8889))
        self.socket.close()


    def get_log(self):
        return self.log