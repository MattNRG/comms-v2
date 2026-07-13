import socket
import struct
import threading
import time
import notify as notify

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))  # Listening on ethernet, Wi-Fi and loopback


# Super proud of this
class Robot:
    def __init__(self, robotid):
        self.id = robotid
        self.addr = None
        self.socket = None
        self.lastSeen = 0
        self.connected = False

        self.onMap = False
        self.position = (0, 0)
        self.rotation = 0
        self.battery = 100

    # Not implemented yet
    def getMessage(self):
        return self.socket.recv(1024)

    # Not implemented yet
    def sendMessage(self, package):
        self.socket.send(package)

    def disconnect(self):
        self.connected = False
        self.socket.close()
        print(f"Robot {self.id}: {self.addr[0]} disconnected")


# Packet handlers unfinished
packets = {
    #1: ('FORMAT', connectRobot),
    #2: ('FORMAT', sendCommands),
    #3: ('FORMAT', getInfo),
    #4: ('FORMAT', setParams),
    #5: ('FORMAT', heartbeat),
    #6: ('FORMAT', stopAll),
}

currentRobots = {}
# Format, robotID: RobotClass

heartBeatTime = 10
checkHeartbeat = 3
loadRobots = 10  # Starts from 0


def addRobots():
    for i in range(loadRobots):
        robotID = str(i)
        robotClass = Robot(robotID)
        currentRobots[robotID] = robotClass

    print(f'Loaded: {currentRobots}')


def checkRobots():
    # Basically heartbeat monitor so robo can connect again
    while True:
        # print(currentRobots)
        for robotID in list(currentRobots):
            # print(f"Checking {robotID}")
            robotClass = currentRobots[robotID]

            if time.time() - robotClass.lastSeen > heartBeatTime and robotClass.connected:
                print(f'Disconnecting {robotID} due to inactivity')
                robotClass.disconnect()
        time.sleep(checkHeartbeat)

    # def connectRobot(client, addr, robotID):
    robotClass = Robot(robotID, addr, client)
    currentRobots[robotID] = robotClass
    print(currentRobots)
    return robotClassc  #


def handleClient(robotid):
    robotClass = currentRobots[robotid]
    print("Connected by: ", robotClass.addr[0])
    while True:
        try:
            # messageType = client.recv(1024).decode()
            # messageType = int(messageType)
            message = robotClass.getMessage().decode()
            print(f"{robotClass.addr[0]}: {message}")
            robotClass.lastSeen = time.time()

            if message == "end":
                break
        except Exception as e:
            print(e)
            break

    if not robotClass.connected:
        return

    robotClass.disconnect()


def startServer():
    print(f"Server created - IP: {socket.gethostbyname(socket.gethostname())}")
    server.listen()
    while True:
        client, addr = server.accept()
        print("New ROBOT connected")

        notify.message("New ROBOT connected", f'IP: {addr[0]}')

        roboid = client.recv(1024).decode()

        currentRobots[roboid].lastSeen = time.time()
        currentRobots[roboid].connected = True
        currentRobots[roboid].addr = addr
        currentRobots[roboid].socket = client

        thread = threading.Thread(target=handleClient, args=roboid, daemon=True)
        thread.start()
        print(f"Currently {threading.active_count() - 2} connection threads active")


addRobots()
threading.Thread(target=startServer, daemon=True).start()
threading.Thread(target=checkRobots(), daemon=True).start()
input("Press enter to stop")
