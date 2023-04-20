import socket
import json 

HOST = "localhost"
PORT = 65432

def Socket(hostIP, hostPort):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((hostIP, hostPort))
        
        s.setblocking(0)

        msg = b""
        print(f"Connected to {hostIP}.")
        while True:
            if s.fileno() == -1:
                print("Closed connection.")
                return
            
            try:
                msg = s.recv(1024)
                print(msg)
            except OSError as e:
                #print(e)
                pass

            if msg != b"":
                try:
                    msg = json.loads(msg.decode("utf-8"))
                    print(msg)
                    msg = b""
                except:
                    pass

if __name__ == "__main__":
    Socket(HOST,PORT)