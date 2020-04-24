import pygame
import math


class Player:
    def __init__(self, x, y, isjump, jumpcount, radius, points):
        self.x = x
        self.y = y
        self.isjump = isjump
        self.jumpcount = jumpcount
        self.radius = radius
        self.points = points


def redraw_game_window(win, bg, player1, player2, ball):  # Wyświetlanie
    win.blit(bg, (0, 0))
    pygame.draw.circle(win, (255, 0, 0), (int(player1.x), int(player1.y)), player1.radius)
    pygame.draw.circle(win, (51, 255, 51), (int(player2.x), int(player2.y)), player2.radius)
    pygame.draw.circle(win, (255, 255, 255), (int(ball.x), int(ball.y)), ball.radius)
    pygame.draw.line(win, (0, 0, 0,), (394, 450), (394, 200))
    pygame.display.update()
    if ball.freeze:
        pygame.time.delay(1000)
        ball.freeze = False
    return ball


def reset(player1, player2, ball, w):  # Reset gry
    player1.x = 50
    player1.y = 414
    player2.x = w - 50
    player2.y = 414
    player1.isjump = False
    player2.isjump = False
    player1.jumpcount = 10
    player2.jumpcount = 10
    ball.x_speed = 0
    ball.y_speed = 0
    ball.freeze = True


def movement(player1, player2, ball, w):  # Fizyka gry
    vel = 6  # Skalowanie szybkości gracza w X
    keys = pygame.key.get_pressed()
    radius_sum = player1.radius + ball.radius
    if ball.y > 444 - ball.radius:  # Sprawdzanie czy piłka upadła
        if ball.x < w / 2:
            player2.points += 1
            ball.x = w - 100
            ball.y = 200
            reset(player1, player2, ball, w)
            print("Player1 ", player1.points, ":", player2.points, "Player2")
            return player1, player2, ball
        else:
            player1.points += 1
            ball.x_speed = 0
            ball.y_speed = 0
            ball.x = 100
            ball.y = 200
            reset(player1, player2, ball, w)
            print("Player1 ", player1.points, ":", player2.points, "Player2")
            return player1, player2, ball

    if keys[pygame.K_LEFT] and player1.x > player1.radius:  # Ruch lewo/prawo
        player1.x -= vel
    elif keys[pygame.K_RIGHT] and player1.x < w / 2 - player1.radius - vel:
        player1.x += vel

    if not player1.isjump:  # Skok
        if keys[pygame.K_UP]:
            player1.isjump = True
    else:
        if player1.jumpcount >= -10:
            player1.y -= player1.jumpcount * abs(player1.jumpcount) * 0.25  # W tych dwóch liniach można
            player1.jumpcount -= 0.5  # przeskalować szybkość/wysokość skoku
        else:
            player1.isjump = False
            player1.jumpcount = 10

    if keys[pygame.K_a] and player2.x > w / 2 + player2.radius + vel:  # Ruch lewo/prawo
        player2.x -= vel
    elif keys[pygame.K_d] and player2.x < w - player2.radius:
        player2.x += vel

    if not player2.isjump:  # Skok
        if keys[pygame.K_w]:
            player2.isjump = True
    else:
        if player2.jumpcount >= -10:
            player2.y -= (player2.jumpcount * abs(player2.jumpcount)) * 0.25
            player2.jumpcount -= 0.5
        else:
            player2.isjump = False
            player2.jumpcount = 10

    ball_y_predict = ball.y + ball.y_speed
    ball_x_predict = ball.x + ball.x_speed
    dist1 = math.sqrt((ball_x_predict - player1.x) ** 2 + (ball_y_predict - player1.y) ** 2)  # Odległości piłka od gracza
    dist2 =  math.sqrt((ball_x_predict - player2.x) ** 2 + (ball_y_predict - player2.y) ** 2)  # Odległości piłka od gracza
    if dist1 <= radius_sum:
        if player1.isjump and player1.jumpcount > 0:
            ball.y_speed = -player1.jumpcount * abs(player1.jumpcount) * 0.18 * ((player1.y - ball.y) / dist1)
        elif player1.isjump and player1.jumpcount < 0:
            ball.y_speed = -30 * (100 - player1.jumpcount ** 2) / 100
        else:
            ball.y_speed = -10
        ball.x_speed = ((ball.x - player1.x) / dist1) * 15
        print("Kolizja1")
    elif dist2 <= radius_sum:
        if player2.isjump and player2.jumpcount > 0:
            ball.y_speed = -player2.jumpcount * abs(player2.jumpcount) * 0.18 * ((player2.y - ball.y) / dist2)
        elif player2.isjump and player2.jumpcount < 0:
            ball.y_speed = -30 * (100 - player2.jumpcount ** 2) / 100
        else:
            ball.y_speed = -10
        ball.x_speed = ((ball.x - player2.x) / dist2) * 15
        print("Kolizja2")


    ball.y_speed += 0.5
    ball.x = ball.x + ball.x_speed  # Przesunięcie piłki
    ball.y = ball.y + ball.y_speed

    real_dist1 = math.sqrt((ball.x - player1.x) ** 2 + (ball.y - player1.y) ** 2)
    real_dist2 = math.sqrt((ball.x - player2.x) ** 2 + (ball.y - player2.y) ** 2)

    if real_dist1 < radius_sum:
        x_dif = ball.x - player1.x
        y_dif = ball.y - player1.y
        if abs(x_dif) < radius_sum:
            ball.x = ball.x + ((radius_sum - abs(x_dif)) / radius_sum) * x_dif
        if abs(y_dif) < radius_sum:
            ball.y = ball.y + ((radius_sum - abs(y_dif)) / radius_sum) * y_dif

    if real_dist2 < radius_sum:
        x_dif = ball.x - player2.x
        y_dif = ball.y - player2.y
        if abs(x_dif) < radius_sum:
            ball.x = ball.x + ((radius_sum - abs(x_dif)) / radius_sum) * x_dif
        if abs(y_dif) < radius_sum:
            ball.y = ball.y + ((radius_sum - abs(y_dif)) / radius_sum) * y_dif

    # if ball.radius > ball.x + ball.x_speed or ball.x + ball.x_speed + ball.radius > w or \
    #         abs(ball.x + ball.x_speed - 394) < ball.radius and ball.y + ball.y_speed > 200 - ball.radius:
    #     ball.x_speed = -ball.x_speed
    if abs(ball.x + ball.x_speed - 394) < ball.radius and ball.y + ball.y_speed > 200 - ball.radius:
        ball.x_speed = -ball.x_speed
    # Odbijanie się piłki od sufitu, podłogi, fajne sprawa, ale trzeba wyłączyć reset przy kontakcie z ziemią
    if ball.x + ball.x_speed + ball.radius < 0 or ball.x + ball.x_speed + ball.radius > w:
        ball.x_speed = -ball.x_speed

    ball.x = ball.x + ball.x_speed  # Przesunięcie piłki
    ball.y = ball.y + ball.y_speed

    return player1, player2, ball


def redraw_game_window_test(win, bg, player, ball):  # Wyświetlanie
    win.blit(bg, (0, 0))
    pygame.draw.circle(win, (255, 0, 0), (int(player.x), int(player.y)), player.radius)
    pygame.draw.circle(win, (255, 255, 255), (int(ball.x), int(ball.y)), ball.radius)
    pygame.display.update()
    if ball.freeze:
        pygame.time.delay(1000)
        ball.freeze = False
    return ball


def movement_test(player, ball, w):
    vel = 4  # Skalowanie szybkości gracza w X
    keys = pygame.key.get_pressed()
    radius_sum = ball.radius + player.radius

    if ball.y > 444 - ball.radius:  # Sprawdzanie czy piłka upadła
        player.points += 1
        ball.x = w/2
        ball.y = 200
        ball.y_speed = 0
        ball.x_speed = 0
        ball.freeze = True
        return player, ball

    if keys[pygame.K_LEFT]:  # Ruch lewo/prawo
        player.x -= vel
    elif keys[pygame.K_RIGHT]:
        player.x += vel

    if not player.isjump:  # Skok
        if keys[pygame.K_UP]:
            player.isjump = True
    else:
        if player.jumpcount >= -10:
            player.y -= player.jumpcount * abs(player.jumpcount) * 0.18  # W tych dwóch liniach można
            player.jumpcount -= 0.25  # przeskalować szybkość/wysokość skoku
        else:
            player.isjump = False
            player.jumpcount = 10

    ball_y_predict = ball.y + ball.y_speed
    ball_x_predict = ball.x + ball.x_speed
    dist = math.sqrt((ball_x_predict - player.x) ** 2 + (ball_y_predict - player.y) ** 2)  # Odległości piłka od gracza

    if dist <= radius_sum:
        if player.isjump and player.jumpcount > 0:
            ball.y_speed = -player.jumpcount * abs(player.jumpcount) * 0.24 * ((player.y - ball.y)/dist)
        elif player.isjump and player.jumpcount < 0:
            ball.y_speed = -30 * (100 - player.jumpcount ** 2) / 100
        else:
            ball.y_speed = -30
        ball.x_speed = ((ball.x - player.x)/dist) * 30
        print("Kolizja")
    ball.y_speed += 2
    ball.x = ball.x + ball.x_speed  # Przesunięcie piłki
    ball.y = ball.y + ball.y_speed

    real_dist = math.sqrt((ball.x - player.x) ** 2 + (ball.y - player.y) ** 2)
    if real_dist < radius_sum:
        x_dif = ball.x - player.x
        y_dif = ball.y - player.y
        if abs(x_dif) < radius_sum:
            ball.x = ball.x + ((radius_sum - abs(x_dif))/radius_sum) * x_dif
        if abs(y_dif) < radius_sum:
            ball.y = ball.y + ((radius_sum - abs(y_dif))/radius_sum) * y_dif

    return player, ball
