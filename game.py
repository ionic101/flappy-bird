import pygame
from settings import *
from models.bird import Bird
from models.level import Level
from UI import UI
from utils import load_sprite
from game_status import GameStatus

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_run = False
        self.game_status: GameStatus = GameStatus.NOT_STARTED

        self.bird = Bird()
        self.level = Level()
        self.ui = UI()

        self.dt = 0.01
        self.score = 1337
        
    
    def tick(self) -> None:
        self.dt = self.clock.tick(MAX_FPS) / 1000

    def read_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_run = False
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT \
                or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) \
                    and self.game_status != GameStatus.GAME_OVER:    
                self.bird.jump()
                self.game_status = GameStatus.IN_GAME
            if self.game_status == GameStatus.GAME_OVER and event.type == pygame.MOUSEBUTTONDOWN \
                and event.button == pygame.BUTTON_LEFT \
                and self.ui.restart_rect.collidepoint(event.pos):
                self.bird.restart()
                self.level.restart()
                self.game_status = GameStatus.NOT_STARTED
                self.score = 0
                
    
    def collide(self) -> None:
        index = self.bird.rect.collidelist(self.level.get_all_rects())
        if index != -1:
            self.game_status = GameStatus.GAME_OVER
    
    def update_score(self) -> None:
        for barrier in self.level.barriers:
            if barrier.center_x > self.bird.x:
                break
            if not barrier.is_passed:
                self.score += 1
                barrier.is_passed = True
    
    def update(self) -> None:
        self.bird.update(self.dt)
        self.level.update(self.dt)
        self.update_score()
    
    def display(self) -> None:
        self.level.display(self.screen)
        self.bird.display(self.screen, self.dt)

        if self.game_status == GameStatus.NOT_STARTED:
            self.ui.display_start_menu(self.screen)
        elif self.game_status == GameStatus.GAME_OVER:
            self.ui.display_game_over(self.screen)
        elif self.game_status == GameStatus.IN_GAME:
            self.ui.display_score(self.screen, self.score)
        
        pygame.display.flip()
    
    def start(self) -> None:
        self.is_run = True
        while self.is_run:
            self.read_events()
            if self.game_status == GameStatus.IN_GAME:
                self.update()
                self.collide()
            self.display()
            self.tick()
