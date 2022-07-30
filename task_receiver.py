# task_receiver.py

import socket
from datetime import datetime
from os import environ
from time import sleep
import os


TCP_IP = '0.0.0.0'
hostname = socket.getfqdn(TCP_IP)
TCP_PORT = 9999
BUFFER_SIZE = 1024


def getTime():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


if __name__ == '__main__':
       
    print("["+getTime()+ "] Getting worker name...")
    worker = environ.get('worker')
    print("["+getTime()+ "] Worker " +str(worker))
    filename = worker
    
    if os.path.exists(os.path.abspath(os.getcwd())+"\\"+filename+".bat"): 
        # run .bat
        os.system("start "+os.path.abspath(os.getcwd())+"\\"+filename+".bat") 
    else:
        print("["+getTime()+ "] Script does not exist")
        
    while True:
        try:    
            
            print("doing stuff")   
            # TODO
            # connect 
            # send worker name
            # receive task
            # write task into file
            # close connection
            # compare new task with old task
            # run new task if different
                
                
        except:
            print("["+getTime()+ "] Something went wrong :(")

            
        sleep(3)
