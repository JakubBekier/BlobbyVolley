import pygame
from PIL import Image

from player import *
from ball import Ball

pygame.init()

pygame.display.set_caption("First game")
bg = pygame.image.load("tlo3.png")
image = Image.open("tlo3.png")
w, h = image.size
win = pygame.display.set_mode((w, h))

player1 = Player(50, 414, False, 10, 30, 0)
player2 = Player(w - 50, 414, False, 10, 30, 0)
playertest = Player(w/2, 414, False, 10, 30, 0)
ball = Ball(100, 200, 0, 0, 20)
balltest = Ball(w/2, 200, 0, 0, 20)

player1_points = 0
player2_points = 0

print(w, h)
run = True
while run:
    pygame.time.delay(30)
    ball = redraw_game_window(win, bg, player1, player2, ball)
    player1, player2, ball = movement(player1, player2, ball, w)
    # balltest = redraw_game_window_test(win, bg, playertest, balltest)
    # playertest, ball = movement_test(playertest, balltest, w)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    print(playertest.jumpcount, balltest.y_speed)
    # print(playertest.x, playertest.y, balltest.x, balltest.y, balltest.y_speed);
pygame.quit()
