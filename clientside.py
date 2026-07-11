import socket
import time

print(f"Current IP: {socket.gethostbyname(socket.gethostname())}")

while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 9999))
        print("Connected")
        while True:
            client.send((input("What to send: ")).encode())
    except:
        print("Connection refused, retrying..")
        time.sleep(1)