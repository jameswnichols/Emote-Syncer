import socket
import json 
import time

HOST = "localhost"
PORT = 65432

NS_TO_MS = 1_000_000

def getTimestamp():
    return time.time_ns()/NS_TO_MS

def Socket(hostIP, hostPort):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((hostIP, hostPort))
    
    s.setblocking(0)

    print(f"Connected to {hostIP}.")
    while True:

        if s.fileno() == -1:
            print("Closed connection.")
            return
        
        try:
            message = json.loads(s.recv(1024).decode("utf-8"))

            messageType, messageData = message["type"], message["data"]

            match messageType:
                case "ping":
                    print(getTimestamp()-messageData["timestamp"])
            


        except OSError as e:
            pass

if __name__ == "__main__":
    Socket(HOST,PORT)