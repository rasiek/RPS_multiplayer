'''
Server to connect the game

'''

import sys
import pickle
import socket
from _thread import *
from player import Player


server = '192.168.1.12'
port = 5555

socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket_1.bind((server, port))
except socket.error as error_1:
    str(error_1)


socket_1.listen(2)
print('Waiting for connection, server started')


players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 255, 0))]

def threaded_client(conn, player):
    
    conn.send(pickle.dumps(players[player]))
    reply = ''

    while True: 
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print('Disconnected')
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print(f'Received {data}')
                print(f'Sending {reply}')

            conn.sendall(pickle.dumps(reply))

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