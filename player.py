import pygame


class Player:
    def __init__(self, x, y, radius, points, colorRGB):
        self.x = x
        self.y = y
        self.isJump = False
        self.jumpCount = 10
        self.radius = radius
        self.points = points
        self.vel = 13           # Było 5
        self.touchBall = False
        self.colorRGB = colorRGB

    def draw(self, win):
        pygame.draw.circle(win, self.colorRGB, (int(self.x), int(self.y)), self.radius)
