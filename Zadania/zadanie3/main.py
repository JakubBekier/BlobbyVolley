import pygame
from textbutton import TextButton

pygame.init()
pygame.display.set_caption("Blobby Volley")
bg = pygame.image.load("background.png")
w, h = 788, 444
win = pygame.display.set_mode((w, h))


run = True
clock = pygame.time.Clock()
button = TextButton(w/2, h/2, "comicsans", 40, "Click!", (0, 0, 0))
while run:
    clock.tick(60)
    button_hover = button.cursor_hover()

    if button_hover:
        button.update("Click!", (0, 200, 0))
    else:
        button.update("Click!", (0, 0, 0))

    win.blit(bg, (0, 0))
    button.draw(win)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_hover:
                run = False