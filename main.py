from sys import argv

from bfsk import BFSK

def main():
    fsk = BFSK()
    
    if argv[1] == "send":
        message = input("Enter message> ")
        fsk.send(message)
    elif argv[1] == "receive":
        fsk.receive()

if __name__ == "__main__":
    main()