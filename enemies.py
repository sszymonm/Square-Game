import pygame
from random import randint, choice
import sys

width=1280
height=720

screen = pygame.display.set_mode((width, height))


class Square:
    def __init__(self, x, y, width, height, color) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def get_pos(self):
        return self.rect

    def move(self):
        pass

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw()
        self.move()

    # def check_border(self):
    #     if self.x <= 0:
    #         self.x = 0
    #     elif self.x >= 1240:
    #         del self

    #     if self.y <= 0:
    #         self.y = 0
    #     elif self.y >= 680:
    #         del self


class Square_player(Square):
    def __init__(self, x, y, width, height, color) -> None:
        super().__init__(x, y, width, height, color)
        self.key_pressed = None
        self.speed = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys == self.key_pressed:
            self.speed += 0.1
        else:
            self.speed = 0
        self.key_pressed = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= 1 + self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += 1 + self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= 1 + self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += 1 + self.speed

        self.check_border()

    def check_border(self):
        if self.x <= 0:
            self.x = 0
        elif self.x >= 1240:
            self.x = 1240

        if self.y <= 0:
            self.y = 0
        elif self.y >= 680:
            self.y = 680


class SquareBotWalkLineX(Square):
    def __init__(
        self, x, y, width, height, color, direction=True
    ) -> None:
        super().__init__(x, y, width, height, color)
        self.direction = direction
        self.delete = False
        # True right ; False left

    def move(self):
        if self.direction:
            if self.x < width+20:
                self.x += 5
            elif self.x >= width+20:
                self.delete=True
        else:
            if self.x > -20:
                self.x -= 5
            elif self.x <= -20:
                self.delete=True


class SquareBotWalkLineY(Square):
    def __init__(
        self, x, y, width, height, color, direction=True
    ) -> None:
        super().__init__(x, y, width, height, color)
        self.direction = direction
        self.delete = False

    def move(self):
        if self.direction:
                if self.y < height+20:
                    self.y += 5
                elif self.y >= height+20:
                    self.delete=True
        else:
                if self.y > -20:
                    self.y -= 5
                elif self.y <= -20:
                    self.delete=True


class Coin(Square):
    def __init__(self, x, y, width=20, height=20, color="yellow"):
        super().__init__(x, y, width, height, color)
        #pygame.time.set_timer(self.end(),5000)
        self.delete = False
        self.timer = 0

    def end_life(self):
        self.delete = True

    def aging(self):
        self.timer += 1
        if self.timer >= 700:
            self.end_life()