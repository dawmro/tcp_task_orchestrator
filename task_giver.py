# task_giver.py


import socket
from threading import Thread
from socketserver import ThreadingMixIn
from datetime import datetime 
from time import sleep
import sqlite3


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
            conn = sqlite3.connect('tasks_'+filename+'.db')
            c = conn.cursor()
            c.execute("""SELECT taskContent FROM Tasks ORDER BY timestamp DESC LIMIT 1""")
            for row in c.fetchall():
                self.sock.send(row[0].encode())
                print("["+getTime()+"] [>]["+str(self.number)+"] Successfully send the file")
                self.sock.shutdown(2)
                self.sock.close()
                print("["+getTime()+"] [-]["+str(self.number)+"] Connection closed")
            c.close()
            conn.close()
        except:
            self.sock.send(("::1603013736\nping 128.0.0.1 -t").encode())
            print("["+getTime()+"] [!]["+str(self.number)+"] Error: Empty template sent instead")
            self.sock.shutdown(2)
            self.sock.close()
            print("["+getTime()+"] [-]["+str(self.number)+"] Connection closed")




if __name__ == '__main__':

    number = 0
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((TCP_IP, TCP_PORT))
    threads = []

    while True:
        number += 1
        tcpsock.listen(5)
        print("["+getTime()+"] [?] Waiting for incoming connections...")
        (conn, (ip,port)) = tcpsock.accept()
        print ("["+getTime()+"] [<] Got connection from "+str(ip)+":"+str(port)+", number: "+str(number))
        newthread = ClientThread(ip,port,conn,number)
        newthread.start()
        threads.append(newthread)
        


