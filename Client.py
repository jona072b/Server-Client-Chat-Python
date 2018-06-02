import socket, threading, Constants

import self as self


class StringLogic:


    def steganography(self,msg):

        pass


    def hash(self,msg):
        pass


    def encryption(self,msg):
        pass


    def ascii(self,msg):
        value = msg[0]
        for c in msg:
            value = str(value) + str(ord(c)) + ","

        return value


class ReverseStringLogic:


    def reverseSteganography(self,msg):
        print("Steganography: " + msg)
        pass

    def reverseHash(self,msg):
        print("Hash: " + msg)
        pass


    def decryption(self,msg):
        print("Encryption: " + msg)
        pass


    def reverseAscii(self,msg):
        print("Ascii: " + msg)
        pass


def recvMessages(meSocket):
    while True:
        data =  mySocket.recv(1024).decode()
        print("Recieved Data")
        first = data[0]

        if first == "1":
            ReverseStringLogic.reverseSteganography(self, data)

        elif first == "2":
            ReverseStringLogic.reverseHash(self, data)

        elif first == "3":
            ReverseStringLogic.decryption(self, data)

        elif first == "4":
            ReverseStringLogic.reverseAscii(self, data)
        else:
            print("Error: " + data)

host = Constants.getIp()
port = Constants.getPort()
messages = ""

mySocket = socket.socket()
mySocket.connect((host,port))

t = threading.Thread(target=recvMessages, args= (mySocket,))
t.start()

while messages!= 'exit':
    messages = input(":")

    first = messages[0]

    if first == "1":
        messages = StringLogic.Steganography(self, messages)

    elif first == "2":
        messages = StringLogic.Hash(self, messages)

    elif first == "3":
        messages = StringLogic.encryption(self, messages)

    elif first == "4":
        messages = StringLogic.ascii(self, messages)
    else:
        print("Error: " + messages)

    print("Sending message: " + messages + "\n")
    mySocket.send(messages.encode())
    print("Message sent.\n")

mySocket.close()