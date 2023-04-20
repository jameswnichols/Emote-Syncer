import socket
import uuid
import time
import select

HOST = "localhost"
PORT = 65432
MS_BETWEEN_PINGS = 1000

NS_TO_MS = 1_000_000

def getTimestamp():
    return time.time_ns()/NS_TO_MS

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

def worker(connectedClient : socket.socket):
    while True:

        #Check if connection is dead
        if connectedClient.fileno() == -1:
            connectedClient.close()
            break


    # while True:
    #     connectedClient.send("OK")
    #     connectedClient.close()

if __name__ == "__main__":
    
    pingController = PingController()

    activeClients = {}

    lastPinged = -1

    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ser.bind((HOST, PORT))
    ser.listen(5)
    ser.setblocking(0)

    while True:
        
        try:
            conn, addr = ser.accept()


        except:
            pass
        
        if lastPinged == -1 or getTimestamp() - lastPinged > MS_BETWEEN_PINGS:
            lastPinged = getTimestamp()
            print("PING")

