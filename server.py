'''
Server to connect the game

'''

import socket
from _thread import *
import sys


server = '192.168.1.12'
port = 5555

socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket_1.bind((server, port))
except socket.error as error_1:
    str(error_1)


socket_1.listen(2)
print('Waiting for connection, server started')


def read_pos(str1):
    str_list = str1.split(',')
    return int(str_list[0]), int(str_list[1])


def make_pos(tup1):
    return str(tup1[0]) + ',' + str(tup1[1])


pos = [(0, 0), (100, 100)]

def threaded_client(conn, player):
    
    print(pos[player])
    conn.send(str.encode(make_pos(pos[player])))
    reply = ''

    while True: 
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data
            print(data)

            if not data:
                print('Disconnected')
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print(f'Received {data}')
                print(f'Sending {reply}')

            conn.sendall(str.encode(make_pos(reply)))

        except:
            break

    
    print('Lost connection')
    conn.close()


current_player = 0

while True:
    conn, addr = socket_1.accept()
    print(f'Connected to {addr}')

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1