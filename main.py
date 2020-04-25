import math
import pygame
from player import *
from ball import Ball

pygame.init()

pygame.display.set_caption("Piłko odbijanko")
bg = pygame.image.load("tlo.png")
w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
bg = pygame.transform.scale(bg, (w, h))
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

player1 = Player(w * 0.05, h - 30, 30, 0, (255, 0, 0))
player2 = Player(w * 0.95, h - 30, 30, 0, (0, 255, 0))
ball = Ball(w * 0.1, h * 0.7, 0, 0, 20)

player1_points = 0
player2_points = 0


def reset(player1, player2, ball, w, h):  # Reset gry
    player1.x = w * 0.05
    player1.y = h - player1.radius
    player2.x = w * 0.95
    player2.y = h - player2.radius
    player1.isJump = False
    player2.isJump = False
    player1.jumpCount = 10
    player2.jumpCount = 10
    ball.x_speed = 0
    ball.y_speed = 0
    ball.freeze = True
    ball.firstTouch = False
    ball.y = 0.75 * h


def movement(player1, player2, ball, w, h):  # Fizyka gry
    keys = pygame.key.get_pressed()
    radius_sum = player1.radius + ball.radius

    if keys[pygame.K_ESCAPE]:
        global run
        run = False

    if ball.y > h - ball.radius:  # Sprawdzanie czy piłka upadła
        if ball.x < w / 2:
            player2.points += 1
            ball.x = 0.9 * w
            reset(player1, player2, ball, w, h)
            print("Player1 ", player1.points, ":", player2.points, "Player2")
            return player1, player2, ball
        else:
            player1.points += 1
            ball.x = 0.1 * w
            reset(player1, player2, ball, w, h)
            print("Player1 ", player1.points, ":", player2.points, "Player2")
            return player1, player2, ball

    if keys[pygame.K_LEFT] and player1.x > player1.radius:  # Ruch lewo/prawo
        player1.x -= player1.vel
    elif keys[pygame.K_RIGHT] and player1.x < w / 2 - player1.radius - player1.vel:
        player1.x += player1.vel

    if not player1.isJump:  # Skok
        if keys[pygame.K_UP]:
            player1.isJump = True
    else:
        if player1.jumpCount >= -10:
            player1.y -= player1.jumpCount * abs(player1.jumpCount) * 0.5  # Było 0.2
            player1.jumpCount -= 0.5
        else:
            player1.isJump = False
            player1.jumpCount = 10

    if keys[pygame.K_a] and player2.x > w / 2 + player2.radius + player2.vel:  # Ruch lewo/prawo
        player2.x -= player2.vel
    elif keys[pygame.K_d] and player2.x < w - player2.radius:
        player2.x += player2.vel

    if not player2.isJump:  # Skok
        if keys[pygame.K_w]:
            player2.isJump = True
    else:
        if player2.jumpCount >= -10:
            player2.y -= (player2.jumpCount * abs(player2.jumpCount)) * 0.5 # Było 0.2
            player2.jumpCount -= 0.5
        else:
            player2.isJump = False
            player2.jumpCount = 10

    players = [player1, player2]
    dist = [math.sqrt((ball.x - player1.x) ** 2 + (ball.y - player1.y) ** 2),
            math.sqrt((ball.x - player2.x) ** 2 + (ball.y - player2.y) ** 2)]

    for player in range(0, 2):
        if dist[player] <= radius_sum:
            ball.firstTouch = True
            if not players[player].touchBall:
                players[player].touchBall = True
                diffx = (ball.x + ball.radius) - (players[player].x + players[player].radius)
                diffy = (ball.y + ball.radius) - (players[player].y + players[player].radius)
                vel = 22.5;   # Było 12.5
                ball.x_speed = diffx / (abs(diffx) + abs(diffy)) * vel;
                ball.y_speed = diffy / (abs(diffx) + abs(diffy)) * vel;
        else:
            players[player].touchBall = False

    player1 = players[0]
    player2 = players[1]

    if ball.firstTouch:
        ball.x += ball.x_speed
        ball.y += ball.y_speed
        ball.y_speed += 0.22;


    if abs(ball.x + ball.x_speed - w/2) < ball.radius and ball.y + ball.y_speed > 0.75 * h - ball.radius:
        ball.x_speed = -ball.x_speed

    if ball.x + ball.x_speed + ball.radius < 0 or ball.x + ball.x_speed + ball.radius > w:
        ball.x_speed = -ball.x_speed

    return player1, player2, ball


def redraw_game_window(win, bg, player1, player2, ball, w, h):  # Wyświetlanie
    win.blit(bg, (0, 0))
    player1.draw(win)
    player2.draw(win)
    ball.draw(win)
    pygame.draw.line(win, (255, 255, 0,), (int(w/2), h), (int(w/2), int(0.6 * h)))
    if ball.y < ball.radius:
        pygame.draw.polygon(win, (0, 0, 0),
                            # Dodaje strzałkę pokazującą gdzie jest piłka w przypadku wylecenia za ekran
                            ((int(ball.x), 6), (int(ball.x) - 6, 12), (int(ball.x) - 2, 8), (int(ball.x) - 2, 26),
                             (int(ball.x) + 2, 26), (int(ball.x) + 2, 8), (int(ball.x) + 6, 12)))
    pygame.display.update()
    if ball.freeze:
        pygame.time.delay(1000)
        ball.freeze = False
    return ball


print(w, h)
run = True
while run:
    clock.tick(75)
    ball = redraw_game_window(win, bg, player1, player2, ball, w, h)
    player1, player2, ball = movement(player1, player2, ball, w, h)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()
