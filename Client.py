import socket, threading, Constants

#receiving method for messages
def recvMessages(meSocket):
    while True:
        data =  mySocket.recv(1024).decode()
        print('Received from server: ' + data)
        #changes to made 1-4

host = Constants.getIp()
port = Constants.getPort()
messages = ""

mySocket = socket.socket()
mySocket.connect((host,port))

t = threading.Thread(target=recvMessages, args= (mySocket,))
t.start()

while messages!= 'exit':
    messages = input(":")
    mySocket.send(messages.encode())

mySocket.close()