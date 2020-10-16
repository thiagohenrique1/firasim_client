import socket

import sys
sys.path.insert(0, './msg')
from packet_pb2 import Environment, Packet
from command_pb2 import Commands, Command

UDP_IP = "127.0.0.1"
UDP_RECEIVE_PORT = 10002
UDP_SEND_PORT = 20011

sock_receive = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock_receive.bind((UDP_IP, UDP_RECEIVE_PORT))

sock_send = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

env = Environment()

while True:
    data, addr = sock_receive.recvfrom(2048)
    env.ParseFromString(data)
    frame = env.frame
    ball = frame.ball
    print("Ball is (x, y) " + str(ball.x) + ", " + str(ball.y))
    for robot in frame.robots_yellow:
        print("yellow Robot (x, y, theta) is " + str(robot.x) + ", " + str(robot.x) + ", " + str(robot.orientation))
    for robot in frame.robots_blue:
        print("blue Robot (x, y, theta) is " + str(robot.x) + ", " + str(robot.x) + ", " + str(robot.orientation))
    
    packet = Packet()
    for i in range(3):
        cmd = Command()
        cmd.id = i
        cmd.yellowteam = False
        cmd.wheel_left = 20
        cmd.wheel_right = 15
        print("sending blue robot " + str(i) + " (VelLeft, VelRight) (rad/s): " + str(cmd.wheel_left) + ", " + str(cmd.wheel_right))
        packet.cmd.robot_commands.append(cmd)
    for i in range(3):
        cmd = Command()
        cmd.id = i
        cmd.yellowteam = True
        cmd.wheel_left = 15
        cmd.wheel_right = 25
        print("sending yellow robot " + str(i) + " (VelLeft, VelRight) (rad/s): " + str(cmd.wheel_left) + ", " + str(cmd.wheel_right))
        packet.cmd.robot_commands.append(cmd)
        
    packet_bytes = packet.SerializeToString()
    sock_send.sendto(packet_bytes, (UDP_IP, UDP_SEND_PORT))
    
