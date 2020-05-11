import pygame

pygame.init()

window = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption(" :-) ")
bg = pygame.image.load("background.png")
bg = pygame.transform.scale(bg, (800, 600))

window.blit(bg, (0, 0))
pygame.draw.circle(window, (255, 0, 0), (200, 300), 15)
pygame.display.update()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()