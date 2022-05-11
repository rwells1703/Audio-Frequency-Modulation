from sys import argv

import mfsk

if __name__ == "__main__":
    if argv[1] == "send":
        message = input("Enter message> ")
        mfsk.send(message)
    elif argv[1] == "receive":
        mfsk.receive()