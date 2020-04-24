import math
import pygame
from player import *
from ball import Ball

pygame.init()

pygame.display.set_caption("First game")
bg = pygame.image.load("tlo3.png")
w, h = 788,444
win = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

player1 = Player(50, 414, 30, 0, (255,0,0))
player2 = Player(w - 50, 414, 30, 0, (0,255,0))
ball = Ball(200, 250, 0, 0, 20)

player1_points = 0
player2_points = 0

def reset(player1, player2, ball, w):  # Reset gry
    player1.x = 70
    player1.y = 414
    player2.x = w - 70
    player2.y = 414
    player1.isJump = False
    player2.isJump = False
    player1.jumpCount = 10
    player2.jumpCount = 10
    ball.x_speed = 0
    ball.y_speed = 0
    ball.freeze = True
    ball.firstTouch = False
    ball.y = 250

def movement(player1, player2, ball, w):  # Fizyka gry
    keys = pygame.key.get_pressed()
    radius_sum = player1.radius + ball.radius

    if ball.y > 444 - ball.radius:  # Sprawdzanie czy piłka upadła
        if ball.x < w / 2:
            player2.points += 1
            ball.x = w - 200
            ball.y = 200
            reset(player1, player2, ball, w)
            print("Player1 ", player1.points, ":", player2.points, "Player2")
            return player1, player2, ball
        else:
            player1.points += 1
            ball.x_speed = 0
            ball.y_speed = 0
            ball.x = 200
            ball.y = 200
            reset(player1, player2, ball, w)
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
            player1.y -= player1.jumpCount * abs(player1.jumpCount) * 0.20  # W tych dwóch liniach można
            player1.jumpCount -= 0.5  # przeskalować szybkość/wysokość skoku
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
            player2.y -= (player2.jumpCount * abs(player2.jumpCount)) * 0.20
            player2.jumpCount -= 0.5
        else:
            player2.isJump = False
            player2.jumpCount = 10

    # mechanika piłki

    #ball_y_predict = ball.y + ball.y_speed
    #ball_x_predict = ball.x + ball.x_speed

    players = [player1, player2]
    dist = [math.sqrt((ball.x - player1.x) ** 2 + (ball.y - player1.y) ** 2),
            math.sqrt((ball.x - player2.x) ** 2 + (ball.y - player2.y) ** 2)]

    for player in range(0,2):
        if dist[player] <= radius_sum:
            ball.firstTouch = True
            if not players[player].touchBall:
                players[player].touchBall = True
                diffx = (ball.x + ball.radius) - (players[player].x + players[player].radius)
                diffy = (ball.y + ball.radius) - (players[player].y + players[player].radius)
                vel = 12.5;
                ball.x_speed = diffx/(abs(diffx)+abs(diffy)) * vel;
                ball.y_speed = diffy/(abs(diffx)+abs(diffy)) * vel;
        else:
            players[player].touchBall = False

    player1 = players[0]
    player2 = players[1]

    if ball.firstTouch:
        ball.x += ball.x_speed
        ball.y += ball.y_speed
        ball.y_speed += 0.22;


    # if ball.radius > ball.x + ball.x_speed or ball.x + ball.x_speed + ball.radius > w or \
    #         abs(ball.x + ball.x_speed - 394) < ball.radius and ball.y + ball.y_speed > 200 - ball.radius:
    #     ball.x_speed = -ball.x_speed
    if abs(ball.x + ball.x_speed - 394) < ball.radius and ball.y + ball.y_speed > 200 - ball.radius:
        ball.x_speed = -ball.x_speed

    # Odbijanie się piłki od sufitu, podłogi, fajne sprawa, ale trzeba wyłączyć reset przy kontakcie z ziemią
    if ball.x + ball.x_speed + ball.radius < 0 or ball.x + ball.x_speed + ball.radius > w:
        ball.x_speed = -ball.x_speed


    return player1, player2, ball

def redraw_game_window(win, bg, player1, player2, ball):  # Wyświetlanie
    win.blit(bg, (0, 0))
    player1.draw(win)
    player2.draw(win)
    ball.draw(win)
    pygame.draw.line(win, (0, 0, 0,), (394, 450), (394, 200))
    pygame.display.update()
    if ball.freeze:
        pygame.time.delay(1000)
        ball.freeze = False
    return ball


print(w, h)
run = True
while run:
    clock.tick(75)
    ball = redraw_game_window(win, bg, player1, player2, ball)
    player1, player2, ball = movement(player1, player2, ball, w)
    # balltest = redraw_game_window_test(win, bg, playertest, balltest)
    # playertest, ball = movement_test(playertest, balltest, w)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #print(player1.y)
    # print(playertest.x, playertest.y, balltest.x, balltest.y, balltest.y_speed);
pygame.quit()