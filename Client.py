import socket, threading

#receiving method for messages
def recvMessages(meSocket):
    while True:
        data =  mySocket.recv(1024).decode()
        print('Received from server: ' + data)
        #changes to made 1-4

host = 'localhost'
port = 5000
messages = ""

mySocket = socket.socket()
mySocket.connect((host,port))

t = threading.Thread(target=recvMessages, args= (mySocket))
t.start()

while messages!= 'q':
    messages = input(":")
    mySocket.send(messages.encode())

mySocket.close()