import pygame
import math
from ball import Ball


class Player:
    def __init__(self, x, y, isjump, jumpcount, x_speed, y_speed, radius):
        self.x = x
        self.y = y
        self.isjump = isjump
        self.jumpcount = jumpcount
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.radius = radius


def redraw_game_window(win, bg, player1, player2, ball):
    win.blit(bg, (0, 0))
    pygame.draw.circle(win, (255, 0, 0), (int(player1.x), int(player1.y)), player1.radius)
    pygame.draw.circle(win, (51, 255, 51), (int(player2.x), int(player2.y)), player2.radius)
    pygame.draw.circle(win, (255, 255, 255), (int(ball.x), int(ball.y)), ball.radius)
    pygame.draw.line(win, (0, 0, 0,), (394, 600), (394, 200))
    pygame.display.update()


def movement(player1, player2, ball, w):
    vel = 10
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player1.x > player1.radius:
        player1.x -= vel
    elif keys[pygame.K_RIGHT] and player1.x < w / 2 - player1.radius - vel:
        player1.x += vel

    if not player1.isjump:
        if keys[pygame.K_UP]:
            player1.isjump = True
    else:
        if player1.jumpcount >= -10:
            player1.y -= player1.jumpcount * abs(player1.jumpcount) * 0.5

            player1.jumpcount -= 1
        else:
            player1.isjump = False
            player1.jumpcount = 10

    if keys[pygame.K_a] and player2.x > w / 2 + player2.radius + vel:
        player2.x -= vel
    elif keys[pygame.K_d] and player2.x < w - player2.radius:
        player2.x += vel

    if not player2.isjump:
        if keys[pygame.K_w]:
            player2.isjump = True
    else:
        if player2.jumpcount >= -10:
            neg = 1
            if player2.jumpcount < 0:
                neg = -1

            player2.y -= (player2.jumpcount ** 2) * 0.5 * neg

            player2.jumpcount -= 1
        else:
            player2.isjump = False
            player2.jumpcount = 10

    dist1 = math.sqrt((ball.x - player1.x)**2 + (ball.y - player1.y)**2)
    dist2 = math.sqrt((ball.x - player2.x)**2 + (ball.y - player2.y)**2)
    if dist1 < ball.radius + player1.radius:
        print("Zderzenie 1")

        if player1.isjump:
            ball.y_speed = - (2*player1.jumpcount - 10)
        else:
            ball.y_speed = - 10
    elif dist2 < ball.radius + player2.radius:
        print("Zderzenie 2")


    ball.y_speed += 2
    ball.x = ball.x + ball.x_speed
    ball.y = ball.y + 0.5*ball.y_speed

    return player1, player2, ball

# Zmienna mówiąca jak długos spada piłka, od niej uzależniona szybkość zmiany y
# Przy uderzeniu zbieramy jumpcount i sprawdzamy jak szybka poruszał się gracz, od tego zależy szybkosc w y
# Zbieramy pozycje gracza i pozycje
# 10 max, 0 bez wpływu, -10 słabiej