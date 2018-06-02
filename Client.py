import socket, threading, Constants


#####################################################
#                   String Logic                    #
#####################################################
import self as self
import hashlib
from cryptography.fernet import Fernet
import io
import os
from PIL import Image


class StringLogic:


    def selfEncryption(self, msg):
        value = msg[:1]
        key = 2
        message = msg[1:]
        result = ""

        for letter in message:
            asciiValue = ord(letter) + key
            finalLetter = chr(asciiValue)
            result = result + finalLetter
        result = value + result
        print(result)

        return result.encode()


    def hash(self, msg):
        value = msg[:1]
        message = msg[1:]
        hashedValue = hashlib.md5(message.encode('utf-8')).hexdigest()
        result = value + hashedValue
        return result.encode()


    def encryption(self,msg):
        value = msg[:1]
        key = Constants.getKey()
        message = msg[1:]
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(str.encode(message))
        string = value + cipher_text.decode("utf-8")
        cipher_text = string.encode()
        return cipher_text


    def ascii(self,msg):
        value = msg[:1]
        message = msg[1:]
        for c in message:
            value = str(value) + str(ord(c)) + ","

        return value[:-1].encode()


#####################################################
#            reverse string logic                   #
#####################################################
import string



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
            asciiValue = ord(letter) - key
            finalLetter = chr(asciiValue)
            result = result + finalLetter

        print(result)

    def bruteForce(self,msg):
        message = msg[1:]
        letterList = string.ascii_lowercase
        for i in letterList:
            for j in letterList:
                for k in letterList:
                    combo = i+j+k
                    hashedCombo = hashlib.md5(combo.encode('utf-8')).hexdigest()
                    if hashedCombo == message:
                        print ("bruteforce: " + combo)



    def decryption(self,msg):
        key = Constants.getKey()
        cipher_suite = Fernet(key)
        plainText = cipher_suite.decrypt(msg[1:].encode())
        print(plainText.decode())

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

        print ("FROM SERVER" + result)





#####################################################
#                   Recieve method                  #
#####################################################


def recvMessages(mySocket):
    while True:
        data = mySocket.recv(1024).decode()
        print("Recieved Data")

        first = data[:1]

        if first == "1":
            ReverseStringLogic.selfDecryption(self,data)

        elif first == "2":
            ReverseStringLogic.bruteForce(self, data)

        elif first == "3":
            ReverseStringLogic.decryption(self, data)

        elif first == "4":
            ReverseStringLogic.reverseAscii(self, data)
        else:
            print("Error: " + data)

#####################################################
#                   MAIN                            #
#####################################################

def Main():

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
            messages = StringLogic.selfEncryption(self, messages)

        elif first == "2":
            messages = StringLogic.hash(self, messages)

        elif first == "3":
            messages = StringLogic.encryption(self,messages)

        elif first == "4":
            messages = StringLogic.ascii(self, messages)
        else:
            print("Error: " + messages)

        #print("Sending message: " + messages + "\n")
        #mySocket.send(messages.encode())
        mySocket.send(messages)
        print("Message sent.\n")

    mySocket.close()

if __name__ == '__main__':
    Main()