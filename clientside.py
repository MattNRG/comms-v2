import socket
import time

roboID = "0"

print(f"Current IP: {socket.gethostbyname(socket.gethostname())}")

while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 9998))
        print("Connected")
        client.send(roboID.encode())
        while True:
            message = input("What to send: ")
            client.send(message.encode())
            if message == "end":
                print("Closing connection")
                client.close()
                time.sleep(3)
                break
    except ConnectionRefusedError as r:
        print(f"{r}; retrying..")
        time.sleep(1)