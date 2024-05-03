# import pygame
# import sys
# from random import randint, choice
from enemies import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.player = Square_player(500, 400, 40, 40, "white")
        self.GameManager = GameManager(self.screen, self.player)
        self.running = False
        self.pause = False
        self.reset = True

        start_font = pygame.font.Font(None, 100)
        self.start_text = start_font.render("Square Game", True, (255, 255, 255))

        start_font = pygame.font.Font(None, 100)
        self.start_text = start_font.render("Square Game", True, (255, 255, 255))

        instruction_font = pygame.font.Font(None, 50)
        self.instruction_text_start = instruction_font.render(
            "Press space to start game", True, (255, 255, 255)
        )

        self.text_the_end = instruction_font.render(
            "Press space to play again", True, (255, 255, 255)
        )

        self.instruction_text_reset = instruction_font.render(
            "Press q to reset game", True, (255, 255, 255)
        )

        self.instruction_text_pause = instruction_font.render(
            "Press p to resume game", True, (255, 255, 255)
        )

        pygame.init()
        # screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Square game")

        clock = pygame.time.Clock()

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.running = True
                elif event.key == pygame.K_q and self.pause == True:
                    self.GameManager.clear()
                    self.GameManager.score = 0
                    self.GameManager.start_game(self.player)
                    self.running = True
                elif event.key == pygame.K_p:
                    if self.running == True:
                        self.running = False
                        self.pause = True
                    else:
                        self.running = True
                        self.pause = False

        if self.running:
            screen.fill((94, 129, 162))

            self.player.update()
            self.GameManager.update()

            if self.GameManager.collision_enemy():
                self.GameManager.first_game = False
                self.reset = True
                self.running = False

            self.GameManager.take_money()

        else:
            self.screen.fill((0, 110, 84))
            screen.blit(self.start_text, (400, 50))

            if self.pause:
                screen.blit(self.instruction_text_pause, (425, 600))
                screen.blit(self.instruction_text_reset, (450, 650))
            else:
                if self.GameManager.first_game:
                    screen.blit(self.instruction_text_start, (425, 600))
                else:
                    screen.blit(self.text_the_end, (425, 600))

                if self.reset == True:
                    self.GameManager.clear()
                    self.GameManager.start_game(self.player)
                    reset = False

        pygame.display.flip()
        clock.tick(60)



class GameManager:
    def __init__(self,screen,player):
        self.square_bots = []
        self.moneys = []
        self.score = 0
        self.font_score = pygame.font.Font(None, 50)
        self.first_game = True
        self.timer_points = 0
        self.screen=screen
        self.player=player

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
            if (self.player.get_pos()).colliderect(self.square_bots[i].get_pos()):
                self.score = 0
                return True

    def take_money(self):
        for i in range(0, len(self.moneys)):
            if (self.player.get_pos()).colliderect(self.moneys[i].get_pos()):
                del self.moneys[i]
                self.score += 1
                return True


pygame.init()
        
        
clock = pygame.time.Clock()
Game = Game()


while True:
    Game.loop()


pygame.quit()
