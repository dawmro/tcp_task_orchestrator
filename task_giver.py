# task_giver.py


import socket
from threading import Thread
from socketserver import ThreadingMixIn
from datetime import datetime 
from time import sleep


TCP_IP = '0.0.0.0'
hostname = socket.getfqdn(TCP_IP)
TCP_PORT = 9999
BUFFER_SIZE = 1024



def getTime():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

class ClientThread(Thread):

    def __init__(self,ip,port,sock,number):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.number = number
        print("["+getTime()+"] [+]["+str(self.number)+"] New thread started for "+str(ip)+":"+str(port))

    def run(self):
        filename = (self.sock.recv(BUFFER_SIZE)).decode()
        print("["+getTime()+"] [<]["+str(self.number)+"] Worker: "+filename)
        try:
            print("try")
            # TODO
            # find task for given worker
            # send task to worker
        except:
            print("except")
            # TODO
            # if no task found send empty task




if __name__ == '__main__':

    number = 0
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    threads = []

    while True:
        print("main loop")
        # TODO
        # listen for new connection
        # run new thread to handle connection
        sleep(1)
        


