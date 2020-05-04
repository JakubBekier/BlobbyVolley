import socket
from _thread import *
from player import Player
from ball import Ball
from game import Game, check_game_state
import pickle
import pygame

server = socket.gethostbyname(socket.gethostname())
port = 5555

w, h = 788,444
players = [Player(50, 414, 30, (255,0,0),30,w/2-30,pygame.K_a,pygame.K_d,pygame.K_w),
           Player(w - 50, 414, 30, (0,255,0), w/2+30, w-30, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)]
ball = Ball(200, 250, 0, 0, 20)
game = Game()
game.pause = True
master_taken = False
guest_taken = False

def get_server_address():
    return server

def threaded_client(conn, player):
    if player == 0:
        conn.send(pickle.dumps([players[0], players[1], ball]))
    else:
        conn.send(pickle.dumps([players[1], players[0], ball]))
    global master_taken, guest_taken
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data or master_taken == False:
                print("Disconnected")
                break
            else:
                players[player], flag_pause, flag_resume = data

                if flag_resume:
                    game.pause = False

                if flag_pause:
                    game.pause = True

                if player == 0:
                    reply = [players[1], ball, game]
                else:
                    reply = [players[0],ball, game]

                if player == 1 and game.pause == False:
                    ball.move(players,game,w)
                    check_game_state(ball, players[0], players[1], game, w)

            conn.send(pickle.dumps(reply))
        except:
            pass

    print("Lost connection")
    print(player)
    conn.close()
    if player == 0:
        master_taken = False
    else:
        guest_taken = False


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    run = True
    global master_taken, guest_taken

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen(2)
    print("Waiting for a connection, Server Started")

    conn, addr = s.accept()
    print("Connected to:", addr)
    master_taken = True
    start_new_thread(threaded_client, (conn, 0))

    while run:
        if master_taken == False:
            run = False

        if guest_taken == False:
            conn, addr = s.accept()
            print("Connected to:", addr)
            guest_taken = True
            game.pause = False
            start_new_thread(threaded_client, (conn, 1))

        pygame.time.delay(1000)

    print("stopping server")
    s.close()
