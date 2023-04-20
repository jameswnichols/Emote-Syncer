import socket
import uuid

HOST = "localhost"
PORT = 65432

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

if __name__ == "__main__":
    pass