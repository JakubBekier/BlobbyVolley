from player import *
from network import Network


pygame.init()
pygame.display.set_caption("Blobby Volley")
bg = pygame.image.load("background.png")
w, h = 788, 444
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

def LAN_game(server_address):
    n = Network(server_address)
    player1, player2, ball, game = n.getP()

    run = True
    while run:
        clock.tick(75)
        player2.x, player2.y, ball, game = n.send([player1.x, player1.y])
        redraw_game_window(win, bg, player1, player2, ball, game)
        player1.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

LAN_game('127.0.0.1')