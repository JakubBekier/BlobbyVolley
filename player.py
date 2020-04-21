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


def redraw_game_window(win, bg, player1, player2, ball):                       # Wyświetlanie
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


def reset(player1, player2, ball, w):                                          # Reset gry
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


def movement(player1, player2, ball, w):                                       # Fizyka gry
    vel = 4                                                                    # Skalowanie szybkości gracza w X
    keys = pygame.key.get_pressed()

    if ball.y > 444 - ball.radius:                                             # Sprawdzanie czy piłka upadła
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
            print("Player1 ", player1.points, ":", player2.points, "Player2")
            return player1, player2, ball

    if keys[pygame.K_LEFT] and player1.x > player1.radius:                     # Ruch lewo/prawo
        player1.x -= vel
    elif keys[pygame.K_RIGHT] and player1.x < w / 2 - player1.radius - vel:
        player1.x += vel

    if not player1.isjump:                                                     # Skok
        if keys[pygame.K_UP]:
            player1.isjump = True
    else:
        if player1.jumpcount >= -10:
            player1.y -= player1.jumpcount * abs(player1.jumpcount) * 0.18     # W tych dwóch liniach można
            player1.jumpcount -= 0.25                                          # przeskalować szybkość/wysokość skoku
        else:
            player1.isjump = False
            player1.jumpcount = 10

    if keys[pygame.K_a] and player2.x > w / 2 + player2.radius + vel:          # Ruch lewo/prawo
        player2.x -= vel
    elif keys[pygame.K_d] and player2.x < w - player2.radius:
        player2.x += vel

    if not player2.isjump:                                                     # Skok
        if keys[pygame.K_w]:
            player2.isjump = True
    else:
        if player2.jumpcount >= -10:
            player2.y -= (player2.jumpcount * abs(player2.jumpcount)) * 0.18
            player2.jumpcount -= 0.25
        else:
            player2.isjump = False
            player2.jumpcount = 10

    dist1 = math.sqrt((ball.x - player1.x) ** 2 + (ball.y - player1.y) ** 2)   # Odległości piłka od gracza
    dist2 = math.sqrt((ball.x - player2.x) ** 2 + (ball.y - player2.y) ** 2)

    if dist1 < ball.radius + player1.radius:
        if player1.isjump:                                                     # Odbicie piłka oś Y
            ball.y_speed = - (3 * player1.jumpcount + 20) / 20                 # Skalowanie odbicia w osi Y
            ball.y = player1.y - ball.radius - player1.radius                  # Przesunięcie piłka za gracze, żeby objekty na siebie nie nachodziły
        else:
            ball.y_speed = - 1                                                 # Odbicie gdy gracz nie porusza się w osi Y
        ball.x_speed = ((ball.x - player1.x) / dist1) * 10                     # Odbicie w X, chujowe, do zmiany, ale jak?
    elif dist2 < ball.radius + player2.radius:                                 # Odbicie dla drugiego gracza
        if player2.isjump:
            ball.y_speed = - (3 * player2.jumpcount + 20) / 10
            ball.y = player2.y - ball.radius - player2.radius
        else:
            ball.y_speed = - 1
        ball.x_speed = ((ball.x - player2.x) / dist2) * 10

    ball.y_speed += 0.05                                                       # Grawitacja

    if ball.radius > ball.x + ball.x_speed or ball.x + ball.x_speed + ball.radius > w or \
            abs(ball.x + ball.x_speed - 394) < ball.radius and ball.y + ball.y_speed > 200 + ball.radius:
        ball.x_speed = -ball.x_speed
    # Odbijanie się piłki od sufitu, podłogi, fajne sprawa, ale trzeba wyłączyć reset przy kontakcie z ziemią
    # if ball.y + ball.y_speed < ball.radius or ball.y + ball.y_speed + ball.radius > 444:
    #     ball.y_speed = -ball.y_speed

    ball.x = ball.x + ball.x_speed                                             # Przesunięcie piłki
    ball.y = ball.y + ball.y_speed

    return player1, player2, ball
