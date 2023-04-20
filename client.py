import socket
import json 
import time
import sys

HOST = "localhost"
PORT = 65432

NS_TO_MS = 1_000_000

def getTimestamp():
    return time.time_ns()/NS_TO_MS

def generatePingPacket(ping):
    return json.dumps({"type":"ping","data":{"ping":ping}}).encode("utf-8")

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
                    s.send(generatePingPacket(getTimestamp()-messageData["timestamp"]))

        except KeyboardInterrupt:
            sys.exit()
            pass

        except json.JSONDecodeError:
            print(f"Disconnected from {HOST}.")
            s.close()
            break

        except:
            pass
        

if __name__ == "__main__":
    Socket(HOST,PORT)