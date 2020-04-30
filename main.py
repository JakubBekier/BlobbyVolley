import math
import pygame
from player import *
from ball import Ball
from network import Network
from server import start_server
from game import Game, check_game_state
from _thread import *

pygame.init()

pygame.display.set_caption("First game")
bg = pygame.image.load("tlo3.png")
w, h = 788,444
print(w, h)
win = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

def redraw_game_window(win, bg, player1, player2, ball, game):  # Wyświetlanie
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


def LAN_game():
    run = True
    n = Network()
    try:
        player1, ball = n.getP()
    except:
        win.blit(bg, (0, 0))
        if confirmation_screen("Cannot connect. Do you want try again?"):
            LAN_game()
        else:
            menu_screen()


    while run:
        clock.tick(75)
        player1, player2, ball, game = n.send(player1)
        redraw_game_window(win, bg, player1, player2, ball,game)
        player1.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if confirmation_screen("Are you sure you want to quit?"):
                run = False
    menu_screen()


def main():
    run = True
    player1 = Player(50, 414, 30, (255, 0, 0), 30, w / 2 - 30, pygame.K_a, pygame.K_d, pygame.K_w)
    player2 = Player(w - 50, 414, 30, (0, 255, 0), w / 2 + 30, w - 30, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)
    ball = Ball(200, 250, 0, 0, 20)
    gs = Game()

    while run:
        clock.tick(75)
        player1.move()
        player2.move()
        ball.move([player1, player2],gs, w)
        check_game_state(ball,player1,player2,gs,w)
        redraw_game_window(win, bg, player1, player2, ball,gs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if confirmation_screen("Are you sure you want to quit?"):
                run = False

    menu_screen()


def check_text_rect_hover(text_rect):
    mpx, mpy = pygame.mouse.get_pos()
    if mpx > text_rect.left and mpx < text_rect.right and mpy > text_rect.top and mpy < text_rect.bottom:
        return True
    else:
        return False

def confirmation_screen(message):
    run = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render(message, True, (0, 0, 0))
    yes = font.render("Yes", True, (200, 0, 0))
    no = font.render("No", True, (0, 0, 0))
    text_rect = text.get_rect()
    yes_rect = yes.get_rect()
    no_rect = no.get_rect()
    text_rect.center = (w // 2, h // 2 - 50)
    yes_rect.center = (w // 2 - 60, h // 2)
    no_rect.center = (w // 2 + 50, h // 2)

    while run:
        clock.tick(60)

        yes_hover = check_text_rect_hover(yes_rect)
        no_hover = check_text_rect_hover(no_rect)

        if yes_hover:
            yes = font.render("Yes", True, (200, 0, 0))
        else:
            yes = font.render("Yes", True, (0, 0, 0))

        if no_hover:
            no = font.render("No", True, (0, 0, 200))
        else:
            no = font.render("No", True, (0, 0, 0))

        win.blit(text, text_rect)
        win.blit(yes, yes_rect)
        win.blit(no, no_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_hover or no_hover:
                    run = False


    if yes_hover:
        return True
    else:
        return False


def menu_screen():
    run = True
    clock = pygame.time.Clock()
    bg = pygame.image.load("tlo3.png")
    font = pygame.font.SysFont("comicsans", 40)
    start_n_game = font.render("START NORMAL GAME", True, (0, 0, 0))
    start_n_game_rect = start_n_game.get_rect()
    start_n_game_rect.center = (w // 2, h // 3)
    start_LAN_game = font.render("START LAN GAME", True, (0, 0, 0))
    start_LAN_game_rect = start_LAN_game.get_rect()
    start_LAN_game_rect.center = (w // 2, h // 2)

    while run:
        clock.tick(60)

        start_n_game_hover = check_text_rect_hover(start_n_game_rect)
        start_LAN_game_hover = check_text_rect_hover(start_LAN_game_rect)

        if start_n_game_hover:
            start_n_game = font.render("START NORMAL GAME", True, (0, 200, 0))
        else:
            start_n_game = font.render("START NORMAL GAME", True, (0, 0, 0))

        if start_LAN_game_hover:
            start_LAN_game = font.render("START LAN GAME", True, (0, 200, 0))
        else:
            start_LAN_game = font.render("START LAN GAME", True, (0, 0, 0))

        win.blit(bg, (0, 0))
        win.blit(start_n_game, start_n_game_rect)
        win.blit(start_LAN_game, start_LAN_game_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_n_game_hover or start_LAN_game_hover:
                    run = False

    if start_n_game_hover:
        main()

    if start_LAN_game_hover:
        server_screen()


def server_screen():
    run = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 40)
    host_game = font.render("HOST GAME", True, (0, 0, 0))
    host_game_rect = host_game.get_rect()
    host_game_rect.center = (w // 2, h // 3)
    join_ex_server = font.render("JOIN EXISTING SERVER", True, (0, 0, 0))
    join_ex_server_rect = join_ex_server.get_rect()
    join_ex_server_rect.center = (w // 2, h // 2)

    while run:
        clock.tick(60)

        host_game_hover = check_text_rect_hover(host_game_rect)
        join_ex_server_hover = check_text_rect_hover(join_ex_server_rect)

        if host_game_hover:
            host_game = font.render("HOST GAME", True, (0, 200, 0))
        else:
            host_game = font.render("HOST GAME", True, (0, 0, 0))

        if join_ex_server_hover:
            join_ex_server = font.render("JOIN EXISTING SERVER", True, (0, 200, 0))
        else:
            join_ex_server = font.render("JOIN EXISTING SERVER", True, (0, 0, 0))

        win.blit(bg, (0, 0))
        win.blit(host_game, host_game_rect)
        win.blit(join_ex_server, join_ex_server_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if host_game_hover or join_ex_server_hover:
                    run = False

    if host_game_hover:
        start_new_thread(start_server,())
        LAN_game()

    if join_ex_server_hover:
        LAN_game()

menu_screen()