import socket, threading, queue, Constants, time

messages = queue.Queue()
clients = []

host = Constants.getIp()
port = Constants.getPort()

mySocket = socket.socket()
mySocket.bind((host,port))
mySocket.listen(1)

"""THREAD FUCTIONS"""

def listenForCLients(socket):
    while True:
        #3-way handshake
        conn, add = socket.accept()

        #Saving to client list
        clients.append(conn)
        print("Client added")
        #Making new thread for new client
        T_newClient = threading.Thread(target= workerClient, args=(conn, messages))
        T_newClient.start()

#This thread recieves messages from clients
def workerClient(connection, msg_queue):
    while True:
        #Changes will be made.
        data = connection.recv(1024).decode()
        print("Message recieved from client: " + data)
        messages.put(data)
        msg_queue.put(data)

def broadcast():
    while True:
        if len(clients) > 0:
            #Make some changes
            print("Sending message to client: " + messages.get())
            sendToAll = str(messages.get()).encode()
            for client in clients:
                client.send(sendToAll)


#Thread that listens for new clients
T_listenForClients = threading.Thread(target=listenForCLients,args=(mySocket,))
T_listenForClients.start()


#Thread for sending out message to all clients
T_broadcast = threading.Thread(target=broadcast)
T_broadcast.start()
