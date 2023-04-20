import socket
import json 
import time
import sys
import os
import subprocess

PLATFORM = sys.platform

DATACENTRE_URL = "ping-eu.ds.on.epicgames.com"

PING_LETTER = "c" if PLATFORM == "darwin" or "linux" in PLATFORM else "n"

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
        try:
            message = json.loads(s.recv(1024).decode("utf-8"))

            messageType, messageData = message["type"], message["data"]

            match messageType:
                case "ping":

                    ret = subprocess.run(f"ping {DATACENTRE_URL} -{PING_LETTER} 1", capture_output=True, shell=True)

                    output = ret.stdout.decode()

                    timeVar = output.find("time=")

                    msVar = output.find("ms")

                    serverPing = float(output[timeVar+5:msVar])

                    s.send(generatePingPacket((getTimestamp()-messageData["timestamp"])+serverPing))

        except KeyboardInterrupt:
            sys.exit()
            pass

        except json.JSONDecodeError:
            print(f"Disconnected from {HOST}.")
            s.close()
            break

        except Exception as e:
            pass
        

if __name__ == "__main__":
    Socket(HOST,PORT)