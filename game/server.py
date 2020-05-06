'''
Server to connect the game

'''

import sys
import pickle
import socket
from _thread import *
from game import Game


server = '192.168.1.12'
port = 5555

socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket_1.bind((server, port))
except socket.error as error_1:
    str(error_1)


socket_1.listen()
print('Waiting for connection, server started')

connected = set()
games = {}
id_count = 0

def threaded_client(conn, player, game_id):
    global  id_count
    conn.send(str.encode(str(player)))

    reply = ''
    while True:
        
        try:
            data = conn.recv(4096).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == 'reset':
                        game.reset_moves()
                    elif data != 'get':
                        game.play(player, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            
            else:
                break
        except:
            break

    print('Lost Connection')
    print('Closing game', game_id)
    try:
        del games[game_id]
    except:
        pass
        id_count -= 1
        conn.close()




while True:
    conn, addr = socket_1.accept()
    print('Connected to:', addr)

    id_count += 1
    current_p = 0
    game_id = (id_count -1)//2


    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print('Creating a new game..')
    else:
        games[game_id].ready = True
        current_p = 1


    start_new_thread(threaded_client, (conn, current_p, game_id))


