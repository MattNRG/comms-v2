import socket
import struct
import threading
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))

# Packet handleres unfinished
packets = {
    #1: ('FORMAT', connectRobot),
    #2: ('FORMAT', sendCommands),
    #3: ('FORMAT', getInfo),
    #4: ('FORMAT', setParams),
    #5: ('FORMAT', heartbeat),
    #6: ('FORMAT', stopAll),
}

currentRobots = {}
# Format, robotID: (IP, PORT), TIME, SOCKET, ACTIVE
# RobotID, TUPLE [0], TIME [1], SOCKET [2], ACTIVE [3]

heartBeatTime = 10

def disconnectRobot(robotID):
    print(f"Robot{robotID}: {currentRobots[robotID][0][0]} disconnected")
    currentRobots[robotID][3] = False
    currentRobots[robotID][2].close()
    del currentRobots[robotID]
    pass

def checkRobots():
    # Basically heartbeat monitor so robo can connect again
    while True:
        for robotID in list(currentRobots):
            if time.time() - currentRobots[robotID][1] > heartBeatTime:
                print(f'Removing {robotID} for inactivity')
                disconnectRobot(robotID)
        time.sleep(1)

def connectRobot(client, addr, robotID):
    if robotID not in currentRobots:
        currentRobots[robotID] = [addr,time.time(), client, True]
        print(currentRobots)
    pass

def handleClient(client, addr):
    print("Connected by: ", addr)

    while True:
        try:
            #messageType = client.recv(1024).decode()
           #messageType = int(messageType)
            message = client.recv(1024).decode()
            print(f"{addr[0]}: {message}")

            if message == "end":
                disconnectRobot(1)
                break
        except:
            break

    client.close()

def startServer():
    print(f"Server; {socket.gethostbyname(socket.gethostname())}")
    server.listen()
    while True:
        client, addr = server.accept()
        print("New ROBOT connected")
        thread = threading.Thread(target=handleClient, args=(client, addr), daemon=True)
        thread.start()
        connectRobot(client, addr, 1)
        print(f"Currently {threading.active_count() - 2} connection threads active")

threading.Thread(target=startServer, daemon=True).start()
threading.Thread(target=checkRobots(), daemon=True).start()
input("Press enter to stop")