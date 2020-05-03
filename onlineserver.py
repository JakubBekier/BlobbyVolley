import socket
from _thread import *
from player import Player
from ball import Ball
from game import Game, check_game_state
import pickle
import pygame
from buffer import Buffer
import sys

#server = '172.104.130.211'
server = '127.0.0.1'
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)


w, h = 788,444
pairs = 5
player1_exemplary = Player(50, 414, 30, (255,0,0),30,w/2-30,pygame.K_a,pygame.K_d,pygame.K_w)
player2_exemplary = Player(w - 50, 414, 30, (0,255,0), w/2+30, w-30, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)
ball_exemplary = Ball(200, 250, 0, 0, 20)

player1_slots_taken = []
player2_slots_taken = []
buffers_player1 = []
buffers_player2 = []
players1 = []
players2 = []
balls = []
buffers_ball1 = []
buffers_ball2 = []
games = []

for i in range(0,pairs):
    player1_slots_taken.append(False)
    players1.append(player1_exemplary)
    buffers_player1.append(Buffer())
    player2_slots_taken.append(False)
    players2.append(player2_exemplary)
    buffers_player2.append(Buffer())
    buffers_ball1.append(Buffer())
    buffers_ball2.append(Buffer())
    balls.append(ball_exemplary)
    games.append(Game())


def get_server_address():
    return server

def threaded_client(conn, player, slot):
    if player == 0:
        conn.send(pickle.dumps([players1[slot], players2[slot], balls[slot], games[slot], player]))
    else:
        conn.send(pickle.dumps([players2[slot], players1[slot], balls[slot], games[slot], player]))

    reply = [Buffer(), Buffer(), games[slot]]
    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("Disconnected")
                break
            else:
                if player1_slots_taken[slot] and player2_slots_taken[slot]:
                    if player == 0:
                        buffers_player1[slot] = data[0]
                        buffers_ball1[slot] = data[1]
                        games[slot].player1_points = data[2]
                        reply = [buffers_player2[slot], buffers_ball2[slot], games[slot].player2_points]
                    else:
                        buffers_player2[slot] = data[0]
                        buffers_ball2[slot] = data[1]
                        games[slot].player2_points = data[2]
                        reply = [buffers_player1[slot], buffers_ball1[slot], games[slot].player1_points]


            conn.send(pickle.dumps(reply))
        except:
            break


    print("Lost connection")
    print("Player " + str(player+1) + " slot " + str(slot))
    conn.close()
    if player == 0:
        player1_slots_taken[slot] = False
    else:
        player2_slots_taken[slot] = False

def reset_game(slot):
    players1[slot] = player1_exemplary
    players2[slot] = player2_exemplary
    buffers_player1[slot] = Buffer()
    buffers_player2[slot] = Buffer()
    balls[slot] = ball_exemplary
    buffers_ball1[slot] = Buffer()
    buffers_ball2[slot] = Buffer()
    games[slot] = Game()

s.listen(pairs*2)
print("Waiting for a connection, Server Started")
run = True
while run:
    conn, addr = s.accept()
    print("Connected to:", addr)

    first_player1_free_slot = pairs
    first_player2_free_slot = pairs
    for i in range(0,pairs):
        if player1_slots_taken[i] == False and i < first_player1_free_slot:
            first_player1_free_slot = i
        if player2_slots_taken[i] == False and i < first_player2_free_slot:
            first_player2_free_slot = i

    if first_player1_free_slot == pairs and first_player2_free_slot == pairs:
        print("No empty slots...")
    else:
        if first_player1_free_slot == first_player2_free_slot:
            print("Player 1 slot " + str(first_player1_free_slot))
            player1_slots_taken[first_player1_free_slot] = True
            start_new_thread(threaded_client, (conn, 0, first_player1_free_slot))
        elif first_player1_free_slot < first_player2_free_slot:
            print("Player 1 slot " + str(first_player1_free_slot))
            reset_game(first_player1_free_slot)
            player1_slots_taken[first_player1_free_slot] = True
            start_new_thread(threaded_client, (conn, 0, first_player1_free_slot))
        else:
            print("Player 2 slot " + str(first_player2_free_slot))
            reset_game(first_player2_free_slot)
            player2_slots_taken[first_player2_free_slot] = True
            start_new_thread(threaded_client, (conn, 1, first_player2_free_slot))
