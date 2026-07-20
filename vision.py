import os
import socket
import struct
import pathlib

if any(
        not os.path.exists('proto/' + proto + '_pb2.py')
        for proto in ('ssl_gc_referee_message', 'ssl_gc_common', 'ssl_gc_game_event', 'ssl_vision_wrapper')
):
    print("Compiling Protobuf files...")
    import grpc_tools.protoc
    grpc_tools.protoc.main([
        'protoc',
        '--python_out=.', '--pyi_out=.',
        *[str(path) for path in pathlib.Path().rglob('proto/*.proto')]
    ])
print("[VISION] Proto files compiled.")
from proto.ssl_vision_wrapper_pb2 import SSL_WrapperPacket

def open_multicast_socket(ip: str, port: int) -> socket.socket:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('' if os.name == 'nt' else ip, port))

    sock.setsockopt(
        socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
        struct.pack('4sl', socket.inet_aton(ip), socket.INADDR_ANY)
    )
    return sock


visionSocket = open_multicast_socket('224.5.23.2', 10006)

def getData():
    data, address = visionSocket.recvfrom(1024)
    print(data)
    # print(data.decode('utf-8'))

    packet = SSL_WrapperPacket()
    packet.ParseFromString(data)

    return packet


print("[VISION] Ready to receive.")