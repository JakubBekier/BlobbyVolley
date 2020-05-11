import pygame

'''
    Uzupełnij klasę TextButton
    Napis powinien być pozycjonowany na ekranie względem środkowych współrzędnych napisu
    Przydatne funkcje:
        mpx, mpy = pygame.mouse.get_post() # zwraca współrzędne kursora myszy
        text.get_rect() # zwraca prostokąt otaczający wyrenderowany text
'''

class TextButton:
    def __init__(self, center_x, center_y, font_name, font_size, text, color):

    def cursor_hover(self):
        # Zwraca True lub False w zależności od tego czy kursor znajduje się nad tekstem

    def update(self, text, color):

    def draw(self,win):
