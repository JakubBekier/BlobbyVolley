import socket
from _thread import *
from player import Player
from ball import Ball
from game import Game, check_game_state, reset
import pickle
import pygame

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

w, h = 788,444
players = [Player(50, 414, 30, (255,0,0),30,w/2-30,pygame.K_a,pygame.K_d,pygame.K_w),
           Player(w - 50, 414, 30, (0,255,0), w/2+30, w-30, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)]
ball = Ball(200, 250, 0, 0, 20)
game = Game()
first_slot = False
second_slot = False

def threaded_client(conn, player):
    conn.send(pickle.dumps([players[player], ball]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = [players[1],players[0],ball,game]
                else:
                    reply = [players[0],players[1],ball,game]

            if player == 1:
                ball.move(players,game,w)
                check_game_state(ball, players[0], players[1], game, w)

            conn.send(pickle.dumps(reply))
        except:
            break


    print("Lost connection")
    conn.close()
    global first_slot, second_slot
    if player == 0:
        first_slot = False
    else:
        second_slot = False


def start_server():
    global first_slot, second_slot

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen(2)
    print("Waiting for a connection, Server Started")

    while True:
        if first_slot == False or second_slot == False:
            conn, addr = s.accept()
            print("Connected to:", addr)

            if first_slot == False:
                first_slot = True
                start_new_thread(threaded_client, (conn, 0))
            elif second_slot == False:
                second_slot = True
                start_new_thread(threaded_client, (conn, 1))

        pygame.time.delay(100)
