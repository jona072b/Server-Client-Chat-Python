import socket, threading, queue, Constants
from self import self
import hashlib
from cryptography.fernet import Fernet


#####################################################
#            reverse string logic                   #
#####################################################
import string

import Logger


def fromValueToList(self, message):
    #Stripping the string from whitespaces in the end and beginning
    string = message.strip()
    #Splitting string on comma
    string = string.split(",")
    return string


class ReverseStringLogic:

    def selfDecryption(self,msg):
        value = msg[:1]
        message = msg[1:]
        key = 2
        result = ""

        for letter in message:
            asciiValue = int(ord(letter) / key)
            finalLetter = chr(asciiValue)
            result = result + finalLetter

        return result

    def bruteForce(self,msg):
        message = msg[1:]
        letterList = string.ascii_lowercase
        for i in letterList:
            for j in letterList:
                for k in letterList:
                    combo = i+j+k
                    hashedCombo = hashlib.md5(combo.encode('utf-8')).hexdigest()
                    if hashedCombo == message:
                        return combo



    def decryption(self,msg):
        key = Constants.getKey()
        cipher_suite = Fernet(key)
        plainText = cipher_suite.decrypt(msg[1:].encode())
        return plainText.decode()

    def reverseAscii(self,msg):
        #Removing first character that is number 4
        message = msg[1:]
        #Variable for holding the end result
        result = ""
        #List for holding the ascii values
        list = fromValueToList(self, message)

        for letter in list:
            #converts numbers to letters
            result = result + chr(int(letter))

        return result





#####################################################
#                   Recieve method                  #
#####################################################


def recvMessages(data, msg_queue,connection):

    first = data[:1]
    message = ""
    if first == "1":
        message = ReverseStringLogic.selfDecryption(self,data)

    elif first == "2":
        message = ReverseStringLogic.bruteForce(self, data)

    elif first == "3":
        message = ReverseStringLogic.decryption(self, data)

    elif first == "4":
        message = ReverseStringLogic.reverseAscii(self, data)
    else:
        print("Error: " + data)


    print("Decrypted message: " + message)

    wordList = message.split(" ")

    fileReader = open("BannedWords.txt","r")
    bannedWords = fileReader.read()
    bannedWords = bannedWords.split("\n")

    numOfBadWords = 0

    for word in wordList:
        for badWord in bannedWords:
            if word == badWord:
                numOfBadWords += 1

    if numOfBadWords > 0:
        messages.put("Illigal use of words, message not sent")
        msg_queue.put("Illigal use of words, message not sent")
        ip = str(connection).split("'")[1]
        logMessage = ip + ": " + message
        Logger.Main(logMessage,numOfBadWords)
    else:
        messages.put(data)
        msg_queue.put(data)
    #Check for words!!



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

        recvMessages(data,msg_queue,connection)

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
