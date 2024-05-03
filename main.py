# import pygame
# import sys
# from random import randint, choice
from enemies import *


class GameManager:
    def __init__(self):
        self.square_bots = []
        self.moneys = []
        self.score = 0
        self.font_score = pygame.font.Font(None, 50)
        self.first_game = True
        self.timer_points = 0

    def generate_enemy(self):
        # choose which type enemy to generate
        # choose direction of enemy
        direction = choice(['topdown','downtop','rightleft','leftright'])

        color=choice(['blue','yellow','green'])
                
        if direction=='topdown':
            place = randint(40,1200)
            self.square_bots.append(SquareBotWalkLineY(place, 0, 40, 40, color, True))
        elif direction=='downtop':
            place = randint(40,1200)
            self.square_bots.append(SquareBotWalkLineY(place, 700, 40, 40, color, False))
        elif direction=='rightleft':
            place = randint(40,700)
            self.square_bots.append(SquareBotWalkLineX(1220, place, 40, 40, color, False))
        else:
            place = randint(40,700)
            self.square_bots.append(SquareBotWalkLineX(0, place, 40, 40, color, True))

    def generate_coins(self):
        coin_x = randint(200,800)
        coin_y = randint(70,400)

        self.moneys.append(Coin(coin_x,coin_y))


    def start_game(self,pl):
        pl.x = 640
        pl.y = 360

    def clear(self):
        self.square_bots.clear()
        self.moneys.clear()

    def update(self):

        self.timer_points += 1

        for i in self.square_bots:
            i.update()

        for i in range(0, len(self.square_bots)):
            if self.square_bots[i].delete==True:
                del self.square_bots[i]
                break

        for i in self.moneys:
            i.draw()
            i.aging()

        for i in range(0,len(self.moneys)):
            if self.moneys[i].delete==True:
                del self.moneys[i]
                break

        score_text = self.font_score.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (1100, 0))

        chance_enemy = randint(0,50)
        if chance_enemy==50:
            self.generate_enemy()

        if len(self.moneys) <= 10:
            chance_money = randint(0,100)

            if chance_money==100:
                self.generate_coins()

        
        if self.timer_points >= 240:
            self.timer_points = 0
            self.score += 1


    def collision_enemy(self):
        for i in range(0, len(self.square_bots)):
            if (player.get_pos()).colliderect(self.square_bots[i].get_pos()):
                self.score = 0
                return True

    def take_money(self):
        for i in range(0, len(self.moneys)):
            if (player.get_pos()).colliderect(self.moneys[i].get_pos()):
                del self.moneys[i]
                self.score += 1
                return True


pygame.init()
# screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Square game")

clock = pygame.time.Clock()
running = False
pause = False

player = Square_player(500, 400, 40, 40, "white")

Game = GameManager()
reset = True

start_font = pygame.font.Font(None, 100)
start_text = start_font.render("Square Game", True, (255, 255, 255))

instruction_font = pygame.font.Font(None, 50)
instruction_text_start = instruction_font.render(
    "Press space to start game", True, (255, 255, 255)
)

text_the_end = instruction_font.render(
    "Press space to play again", True, (255, 255, 255)
)

instruction_text_reset = instruction_font.render(
    "Press q to reset game", True, (255, 255, 255)
)

instruction_text_pause = instruction_font.render(
    "Press p to resume game", True, (255, 255, 255)
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = True
            elif event.key == pygame.K_q and pause == True:
                Game.clear()
                Game.score = 0
                Game.start_game(player)
                running = True
            elif event.key == pygame.K_p:
                if running == True:
                    running = False
                    pause = True
                else:
                    running = True
                    pause = False

    if running:
        screen.fill((94, 129, 162))

        player.update()
        Game.update()

        if Game.collision_enemy():
            Game.first_game = False
            reset = True
            running = False

        Game.take_money()

    else:
        screen.fill((0, 110, 84))
        screen.blit(start_text, (400, 50))

        if pause:
            screen.blit(instruction_text_pause, (425, 600))
            screen.blit(instruction_text_reset, (450, 650))
        else:
            if Game.first_game:
                screen.blit(instruction_text_start, (425, 600))
            else:
                screen.blit(text_the_end, (425, 600))

            if reset == True:
                Game.clear()

                Game.start_game(player)
                reset = False

    pygame.display.flip()
    clock.tick(60)


pygame.quit()