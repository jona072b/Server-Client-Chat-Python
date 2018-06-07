
data = input("What word do you want to search for?\n")

readLog = open("logger.log","r")

for line in readLog.readlines():
    if data in line:
        print(line,end="")