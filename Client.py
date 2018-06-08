import socket, threading, Constants
import self as self
import hashlib
from cryptography.fernet import Fernet


#####################################################
#                   String Logic                    #
#####################################################

class StringLogic:

    #SelfEncryption method, a method for encryption I have made myself, with a key.
    def selfEncryption(self, msg):
        value = msg[:1]
        key = 2
        message = msg[1:]
        result = ""

        for letter in message:
            #Takes the ascii value and multiplies it with the key for encryption
            asciiValue = ord(letter) * key
            #Finds the letter for the final ascii value
            finalLetter = chr(asciiValue)
            result = result + finalLetter
        result = value + result

        return result.encode()

    #Hash method. This hashes the value og a string
    def hash(self, msg):
        value = msg[:1]
        message = msg[1:]
        hashedValue = hashlib.md5(message.encode('utf-8')).hexdigest()
        result = value + hashedValue
        return result.encode()

    #Encryption method from module Fernet
    def encryption(self,msg):
        value = msg[:1]
        key = Constants.getKey()
        message = msg[1:]
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(str.encode(message))
        string = value + cipher_text.decode("utf-8")
        cipher_text = string.encode()
        return cipher_text

    #Takes the ascii values from the letters and seperates them with commas
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


#this takes a string that is seperated by commas and makes them into a list
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


def recvMessages(mySocket):
    while True:
        data = mySocket.recv(1024).decode()
        print("Recieved message: " + data)

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

        print("Recieved Message: " + message)

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
        messages = input("Write your message here:\n")

        first = input("What way do you want to send your message?\n1. Easy Encryption\n2. Hash (If sending with hash, no more than 3 letters only lowercase)\n"
                      "3. Real encryption\n4. Scramble with ASCII\n")

        fullMessage = first + messages

        if first == "1":
            messages = StringLogic.selfEncryption(self, fullMessage)

        elif first == "2":
            messages = StringLogic.hash(self, fullMessage)

        elif first == "3":
            messages = StringLogic.encryption(self,fullMessage)

        elif first == "4":
            messages = StringLogic.ascii(self, fullMessage)
        else:
            print("Error: " + fullMessage)


        mySocket.send(messages)

    mySocket.close()

if __name__ == '__main__':
    Main()