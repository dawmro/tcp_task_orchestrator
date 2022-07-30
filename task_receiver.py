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
        # run task
        os.system("start "+os.path.abspath(os.getcwd())+"\\"+filename+".bat") 
    else:
        print("["+getTime()+ "] Script does not exist")
        
    while True:
        try:

            print("\n["+getTime()+ "] Worker: "+str(worker))
            print("["+getTime()+ "] Creating socket...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connect
            print("["+getTime()+ "] Connecting...")
            s.connect((hostname, TCP_PORT))
            # send worker name
            print("["+getTime()+ "] Sending...")
            s.send(filename.encode())
            
            with open(os.path.abspath(os.getcwd())+"\\"+filename+".tsk", 'wb') as f:
                print("["+getTime()+"] File opened")
                while True:
                    # receive task
                    print("["+getTime()+ "] Receiving data...")
                    data = s.recv(BUFFER_SIZE)

                    if not data:
                        f.close()
                        print("["+getTime()+"] File closed")
                        break
                    # write task into file
                    f.write(data)
                    
            # close connection
            print("["+getTime()+"] File received successfully")
            s.shutdown(2)
            s.close()
            print("["+getTime()+"] Connection closed")
            
            taskContent = ''
            batContent = ''
            doStuff = 0
            with open(os.path.abspath(os.getcwd())+"\\"+filename+".tsk", 'r') as f:
                taskContent = f.readlines()
            print("["+getTime()+ "] Task Timestamp: "+taskContent[0].replace("::", "").replace("\n", ""))
        
            if os.path.exists(os.path.abspath(os.getcwd())+"\\"+filename+".bat"):
                print("["+getTime()+ "] Script exist")
                if os.stat(os.path.abspath(os.getcwd())+"\\"+filename+".bat").st_size == 0:
                    print("["+getTime()+ "] Script size = 0")
                    with open(os.path.abspath(os.getcwd())+"\\"+filename+".bat", 'w') as f:
                        for line in taskContent:
                            f.write(str(line))
                    print("["+getTime()+ "] Script overwritten")
                    # run .bat
                    os.system("start "+os.path.abspath(os.getcwd())+"\\"+filename+".bat")
                else:
                    print("["+getTime()+ "] Script size > 0") 
            else:
                print("["+getTime()+ "] Script does not exist")
                with open(os.path.abspath(os.getcwd())+"\\"+filename+".bat", 'w') as f:
                    for line in taskContent:
                        f.write(str(line))
                print("["+getTime()+ "] Script created")
                # run .bat
                os.system("start "+os.path.abspath(os.getcwd())+"\\"+filename+".bat")

            # compare new task with old task
            with open(os.path.abspath(os.getcwd())+"\\"+filename+".bat", 'r') as f:
                batContent = f.readlines()
            print("["+getTime()+ "] Script Timestamp: "+batContent[0].replace("::", "").replace("\n", ""))
            
            
            if int(taskContent[0].replace("::", "").replace("\n", "")) == int(batContent[0].replace("::", "").replace("\n", "")):
                print("["+getTime()+ "] No new tasks")
            else:
                print("["+getTime()+ "] New task found!")
                with open(os.path.abspath(os.getcwd())+"\\"+filename+".bat", 'w') as f:
                    for line in taskContent:
                        f.write(str(line))
                print("["+getTime()+ "] Script updated")
                # reboot if new task is different
                print("["+getTime()+ "] Rebooting...")
                os.system("call shutdown /r /t 15 /f")
                
            print("["+getTime()+ "] Waiting for the right moment...")    


        except:
            print("["+getTime()+ "] Something went wrong :(")

            
        sleep(30)
