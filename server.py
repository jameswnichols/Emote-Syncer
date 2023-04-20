import socket
import uuid
import time
import select
import multiprocessing as mp
import json
import pynput

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
MS_BETWEEN_PINGS = 1000

NS_TO_MS = 1_000_000

def getTimestamp():
    return time.time_ns()/NS_TO_MS

def generatePingPacket():
    return json.dumps({"type":"ping","data":{"timestamp":getTimestamp()}}).encode("utf-8")

class PingAverage:
    def __init__(self):
        self.amountOfPings = 0
        self.averagePing = 0
        self.pingList = []
        
    def addPing(self, value):
        self.pingList.append(value)
        self.amountOfPings += 1
        self.averagePing = sum(self.pingList) // self.amountOfPings
        return self.averagePing

    def getPing(self):
        return self.averagePing

class PingController:
    def __init__(self):
        self.pingValues = {}

    def addUser(self):
        userID = uuid.uuid4()
        self.pingValues[userID] = PingAverage()
        return userID

    def addPingValue(self, userID, value):
        self.pingValues[userID].addPing(value)
    
    def getPingValue(self, userID):
        return self.pingValues[userID].getPing()
    
    def removeUser(self, userID):
        del self.pingValues[userID]

def worker(connectedClient : socket.socket, pingController : PingController, clientID, rec):
    print(f"{clientID} connected.")

    pingCounter = 1

    while True:
        #Receive messages from main core
        try:
            match rec.recv():
                case "ping":
                    #Check if client doesnt respond to pings
                    if pingCounter % 2 != 0 and pingCounter != 1:
                        raise Exception
                    
                    pingCounter += 1
                    connectedClient.send(generatePingPacket())
        except:
            
            #If client connection is dead 
            connectedClient.close()
            pingController.removeUser(clientID)
            print(f"{clientID} disconnected.")
            break
        
        #Receive messages from client
        try:
            message = json.loads(connectedClient.recv(1024).decode("utf-8"))

            messageType, messageData = message["type"], message["data"]

            match messageType:
                case "ping":
                    pingCounter += 1
                    pingController.addPingValue(clientID, messageData["ping"])

        except:
            pass


if __name__ == "__main__":
    
    pingController = PingController()

    activeClients = {}

    lastPinged = -1

    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ser.bind((HOST, PORT))
    ser.listen(5)
    ser.setblocking(0)

    print(f"Started hosting {HOST} on port {PORT}")

    while True:
        
        try:
            #Runs when knew client attempts to join.
            conn, addr = ser.accept()
            clientID = pingController.addUser()

            rec, send = mp.Pipe()

            activeClients[clientID] = (mp.Process(target=worker, args=(conn, pingController, clientID, rec)),send)

            activeClients[clientID][0].daemon = True

            activeClients[clientID][0].start()

        except Exception as e:
            #When no new clients are trying to join.
            pass
        
        #Sends out a ping to the clients every second.
        if lastPinged == -1 or getTimestamp() - lastPinged > MS_BETWEEN_PINGS:
            lastPinged = getTimestamp()

            currentIndex = 0

            while currentIndex < len(activeClients):
                clientID, data = list(activeClients.keys())[currentIndex], list(activeClients.values())[currentIndex]

                if not data[0].is_alive():
                    print(f"Prune {clientID}.")
                    del activeClients[clientID]
                    currentIndex += 1
                    continue

                data[1].send("ping")
                
                currentIndex += 1
                    

