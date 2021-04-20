import socket
import threading
import json




class ClientThread(threading.Thread):

    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.csocket = clientSocket
        print("New connection added: ", clientAddress)
        
    def run(self):

        print("Connection from: ", clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            print("COMPUTER: ", msg)
            self.csocket.send(bytes(msg, 'utf-8'))

            data = self.csocket.recv(2048)
            msg = json.loads(data) 
            print("JSON: ", msg)
            self.csocket.send(data)

            data = self.csocket.recv(2048)
            msg = data.decode()
            print("DONE RECIEVING: ", msg)
            self.csocket.send(bytes(msg, 'utf-8'))

            if msg == 'DONE':
                break
        print("Client at ", clientAddress, " disconnected...")
        
# LOCALHOST -> Server host IP
LOCALHOST = "129.65.134.233"
# PORT -> Port opened for server to client connection
PORT = 2457

# bind the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(5)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()