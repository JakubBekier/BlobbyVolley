import pygame

class Ball:
    def __init__(self, x, y, x_speed, y_speed, radius, freeze=False):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.radius = radius
        self.freeze = freeze
        self.firstTouch = False

    def draw(self,win):
        pygame.draw.circle(win, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
