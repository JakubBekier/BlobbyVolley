import pygame
import copy
from ball import Ball
from network import Network
from game import Game
from _thread import *
from textpanel import TextPanel
from buffer import Buffer


pygame.init()
pygame.display.set_caption("Blobby Volley")
bg = pygame.image.load("background.png")
w, h = 788, 444
print(w, h)
win = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

def redraw_game_window(win, bg, player1, player2, ball, game):
    win.blit(bg, (0, 0))
    ball.draw(win)
    player1.draw(win)
    player2.draw(win)
    pygame.draw.line(win, (0, 0, 0,), (394, 450), (394, 200))
    game.show_stats(w, h, win)
    if ball.y < ball.radius:
        pygame.draw.polygon(win, (0, 0, 0),
        # Dodaje strzałkę pokazującą gdzie jest piłka w przypadku wylecenia za ekran
        ((int(ball.x), 6), (int(ball.x) - 6, 12), (int(ball.x) - 2, 8), (int(ball.x) - 2, 26),
        (int(ball.x) + 2, 26), (int(ball.x) + 2, 8), (int(ball.x) + 6, 12)))
    pygame.display.update()


game = Game()
opponent_connected = False
buffer_player1 = Buffer()
buffer_player1_recv = Buffer()
buffer_player2 = Buffer()
buffer_ball = Buffer()
def thread_updating_data(n,c):
    '''
    Należy cylkiczne wysyłać bufor naszego gracza
    n.send(plik) -> wysyła plik do serwera w odpowiedzi otrzymujemy tablicę
        [buffer_player1 (naszego gracza), buffer_player2, buffer_ball, game, opponent_connected]
    '''

def online_game(server_address):
    n = Network(server_address)
    global buffer_player1, buffer_player1_recv, buffer_player2, buffer_ball, game, ball, opponent_connected
    player1, player2, ball, game, opponent_connected = n.get_init_data()
    player1_recv = copy.copy(player1)

    print("connected")
    start_new_thread(thread_updating_data, (n,0))

    run = True
    while run:
        clock.tick(75)
        keys = pygame.key.get_pressed()

        if opponent_connected == False:
            game = Game()
            ball = Ball(200, 250, 0, 0, 20)
            waiting_screen()
        else:
            player1.move() # zmienia położenie gracza w zależności od wciśniętych przycisków
            '''
            Zaimplementuj odpowiednią obsługę buforów
            Player.x, Player.y oraz Ball.x, Ball.y określają współrzędne położenia obiektów
            Bufory gracza i piłki skłądaja się z tablicy współrzędnych położenia
            '''

        redraw_game_window(win, bg, player1_recv, player2, ball, game)
        if game.is_game_over():
            n.disconnect()
            game_over_screen(game)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if keys[pygame.K_ESCAPE]:
            run = False


def waiting_screen():
    text = TextPanel(w // 2, h // 3.4, "comicsans", 34, "Waiting for opponent...", (0, 0, 0))
    text.draw(win)
    pygame.display.update()
    pygame.time.delay(50)

def game_over_screen(game):
    if game.left_player_points > game.right_player_points:
        text = TextPanel(w / 2, h / 3, "comicsans", 40, game.left_player_name + " has won the game", (0, 0, 0))
    else:
        text = TextPanel(w / 2, h / 3, "comicsans", 40, game.right_player_name + " has won the game", (0, 0, 0))
    text.draw(win)
    pygame.display.update()
    pygame.time.delay(3000)



online_game('172.104.130.211')
#online_game('127.0.0.1')