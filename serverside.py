import socket
import struct
import threading
import time
import notify as notify # Debug use only

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9998))  # Listening on ethernet, Wi-Fi and loopback


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

    def getMessage(self):
        return self.socket.recv(1024)

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
loadRobots = 1  # Starts from 0


def addRobots():
    for i in range(loadRobots):
        robotID = str(i)
        robotClass = Robot(robotID)
        currentRobots[robotID] = robotClass

    print('Robots loaded successfully')


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
            print(f"Robot {robotClass.id}: {message}")
            robotClass.lastSeen = time.time()

            if message == "end" or message == "":
                break

        except Exception as Error:
            print(Error)
            break

    if not robotClass.connected:
        return

    robotClass.disconnect()
    print("Ending thread")

# Readding so we can safely connect robots (currently it can cause memory leakage)
def connectRobot(client, addr, robotid):

    if currentRobots[robotid].connected:
        currentRobots[robotid].socket.close()

    currentRobots[robotid].lastSeen = time.time()
    currentRobots[robotid].connected = True
    currentRobots[robotid].addr = addr
    currentRobots[robotid].socket = client



def startServer():
    print(f"IP: {socket.gethostbyname(socket.gethostname())}")
    server.listen()
    while True:
        client, addr = server.accept()

        robotid = client.recv(1024).decode()
        connectRobot(client, addr, robotid)

        notify.message(f"ROBOT{robotid} connected", f'IP: {addr[0]}')

        thread = threading.Thread(target=handleClient, args=robotid, daemon=True)
        thread.start()
        print(f"Currently {threading.active_count() - 2} connection threads active")


addRobots()
threading.Thread(target=startServer, daemon=True).start()
threading.Thread(target=checkRobots(), daemon=True).start()
input("Press enter to stop")
