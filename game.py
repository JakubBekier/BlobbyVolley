import pygame

class Game:
    def __init__(self):
        self.player1_points = 0
        self.player2_points = 0
        self.player1_touches = 0
        self.player2_touches = 0
        self.player1_series = False
        self.player2_series = False
        self.player1_name = "Player1"
        self.player2_name = "Player2"

    def player1_got_point(self):
        print("Player1 got point")
        if self.player1_series:
            self.player1_points += 1
        else:
            self.player1_series = True
            self.player2_series = False

    def player2_got_point(self):
        print("Player2 got point")
        if self.player2_series:
            self.player2_points += 1
        else:
            self.player2_series = True
            self.player1_series = False

    def player1_touch(self):
        self.player2_touches = 0
        self.player1_touches += 1

    def player2_touch(self):
        self.player1_touches = 0
        self.player2_touches += 1

    def if_end_of_game(self):
        if abs(self.player1_points - self.player2_points) >= 2:
            if self.player1_points >= 2:
                return True
            elif self.player2_points >= 2:
                return True
        else:
            return False

    def show_stats(self,w,h,win):
        font = pygame.font.Font('freesansbold.ttf', 25)
        text1 = self.player1_name + ': ' + str(self.player1_points)
        text2 = self.player2_name + ': ' + str(self.player2_points)
        if self.player1_series:
            text1 += '!'
        if self.player2_series:
            text2 += '!'
        text1 = font.render(text1, True, (0, 0, 0))
        text2 = font.render(text2, True, (0, 0, 0))
        text_rect1 = text1.get_rect()
        text_rect2 = text2.get_rect()
        text_rect1.center = (w // 4, 20)
        text_rect2.center = (w // 4 + w // 2, 20)
        win.blit(text1, text_rect1)
        win.blit(text2, text_rect2)


def reset(player1, player2, ball, gs, w):  # Reset gry
    player1.x = 70
    player1.y = 414
    player2.x = w - 70
    player2.y = 414
    player1.isJump = False
    player2.isJump = False
    player1.jumpCount = 10
    player2.jumpCount = 10
    ball.x_speed = 0
    ball.y_speed = 0
    ball.freeze = True
    ball.firstTouch = False
    ball.y = 250
    gs.player1_touches = 0
    gs.player2_touches = 0

def check_game_state(ball,player1,player2,gs,w):
    if ball.y > 444 - ball.radius:  # Sprawdzanie czy piłka upadła
        if ball.x < w / 2:
            gs.player2_got_point()
            ball.x = w - 200
            ball.y = 200
        else:
            gs.player1_got_point()
            ball.x = 200
            ball.y = 200

        print("Player1 ", gs.player1_points, ":", gs.player2_points, "Player2")
        reset(player1, player2, ball,gs, w)

    elif gs.player1_touches == 4:
        gs.player2_got_point()
        ball.x = w - 200
        ball.y = 200
        print("Player1 ", gs.player1_points, ":", gs.player2_points, "Player2")
        reset(player1, player2, ball, gs, w)

    elif gs.player2_touches == 4:
        gs.player1_got_point()
        ball.x = 200
        ball.y = 200
        print("Player1 ", gs.player1_points, ":", gs.player2_points, "Player2")
        reset(player1, player2, ball, gs, w)
    else:
        pass