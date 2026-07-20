import colorama
import socket
import struct
import threading
import time
import notify as notify  # Debug use only
from vision import visionClient

from colorama import Fore, Back
colorama.init(autoreset=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9997))  # Listening on everything

class Ball:
    def __init__(self):
        self.position = (0, 0)

class Robot:
    def __init__(self, robotid):
        self.id = robotid
        self.addr = 0
        self.socket = None
        self.lastSeen = 0
        self.connected = False

        self.onMap = False
        self.position = (0, 0)
        self.rotation = 0
        self.battery = 100
        self.gyroRotation = 0

    def __repr__(self):
        return f"Robot {self.id} {self.addr[0]}, battery: {self.battery}, gyro: {self.gyroRotation}, on field map: {self.position}"

    def getMessage(self):
        return self.socket.recv(1024)

    def sendMessage(self, package):
        self.socket.send(package)

    def disconnect(self):
        self.connected = False
        self.socket.close()
        print(Fore.YELLOW + f"[ROBOT {self.id}] {self.addr[0]} disconnected")


loadedRobots = {}
heartBeatTime = 10
checkHeartbeat = 3
loadRobots = 12  # Starts from 0


def unpack(packet, robotClass):

    # 1 Send commands
    # 2 Get info
    # 3 Set params
    # 4 Heartbeat
    # 5 Stop all
    # 6 Error?
    # 7 Message
    #print(f'[DEBUG] Packet: {packet}')

    packetType = packet[0]
    robotClass.lastSeen = time.time()
    match packetType:  # Can be expanded later
        case 2:
            packetType, battery, gyroRotation = struct.unpack('BBB', packet)
            robotClass.battery = battery
            robotClass.gyroRotation = gyroRotation
        case 4:
            robotClass.lastSeen = time.time()
        case 7:
            print(f'[ROBOT {robotClass.id}] {packet.decode()}')
            pass

def addRobots():
    for i in range(loadRobots):
        robotID = str(i)
        robotClass = Robot(robotID)
        loadedRobots[robotID] = robotClass

    print('[SERVER] Robots loaded successfully')


def checkRobots():
    # Basically heartbeat monitor so robo can connect again
    while True:
        # print(loadedRobots)
        for robotID in list(loadedRobots):
            # print(f"Checking {robotID}")
            robotClass = loadedRobots[robotID]

            if time.time() - robotClass.lastSeen > heartBeatTime and robotClass.connected:
                print(Back.RED + f'[SERVER] Disconnecting {robotID} due to inactivity')
                robotClass.disconnect()
        time.sleep(checkHeartbeat)


def handleRobot(robotid):
    robotClass = loadedRobots[robotid]
    while True:
        try:
            message = robotClass.getMessage()

            unpack(message, robotClass)

            if message == "end" or message == "":
                break

        except Exception as Error:
            print(Back.RED + f'Ending thread due to {Error}')
            break

    if not robotClass.connected:
        return

    robotClass.disconnect()
    print(Fore.YELLOW + "[SERVER] Ending thread")


def startServer():
    server.listen()
    while True:
        client, addr = server.accept()

        robotid = client.recv(1024).decode()
        print(robotid)

        if loadedRobots[robotid].connected:
            loadedRobots[robotid].socket.close()

        loadedRobots[robotid].lastSeen = time.time()
        loadedRobots[robotid].connected = True
        loadedRobots[robotid].addr = addr
        loadedRobots[robotid].socket = client

        notify.message(f"[SERVER] ROBOT {robotid} connected", f'IP: {addr[0]}')
        print(Back.GREEN + f'[SERVER] ROBOT {robotid} connected IP: {addr[0]}')

        thread = threading.Thread(target=handleRobot, args=robotid, daemon=True)
        thread.start()
        print(f"[SERVER] Currently {threading.active_count() - 2} connection threads active")


addRobots()
print(Back.GREEN + "        READY TO START        ")
threading.Thread(target=startServer, daemon=True).start()
threading.Thread(target=checkRobots, daemon=True).start()
print(Fore.LIGHTRED_EX + f"Server IP: {socket.gethostbyname(socket.gethostname())}")
input("ENTER TO CLOSE ALL THREADS")
print(Back.RED + "       PROCESS FINISHED       ")