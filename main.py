import pygame
from PIL import Image

from classes import *
from ball import Ball

pygame.init()

pygame.display.set_caption("First game")
bg = pygame.image.load("tlo3.png")
image = Image.open("tlo3.png")
w, h = image.size
win = pygame.display.set_mode((w, h))

player1 = Player(50, 414, False, 10, 0, 0, 30)
player2 = Player(w - 50, 414, False, 10, 0, 0, 30)
ball = Player(100, 200, False, 0, 0, 0, 20)
run = True
while run:
    pygame.time.delay(30)
    player1, player2, ball = movement(player1, player2, ball, w)
    redraw_game_window(win, bg, player1, player2, ball)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
