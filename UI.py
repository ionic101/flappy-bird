import pygame
from utils import load_sprite
from settings import *


class UI:
    def __init__(self) -> None:
        self.start_menu = load_sprite('assets/sprites/start_menu.png')
        self.start_menu_rect = self.start_menu.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.game_over = load_sprite('assets/sprites/game_over.png')
        self.game_over_rect = self.game_over.get_rect(center=(SCREEN_WIDTH // 2, 300))

        self.restart = load_sprite('assets/sprites/restart.png')
        self.restart_rect = self.restart.get_rect(center=(SCREEN_WIDTH // 2, 800))

        self.digits = [load_sprite(f'assets/sprites/digits/{i}.png') for i in range(10)]
    
    def get_score_sprites(self, score: int) -> list[pygame.Surface]:
        return [self.digits[int(i)] for i in str(score)]

    def display_start_menu(self, screen: pygame.Surface) -> None:
        screen.blit(self.start_menu, self.start_menu_rect)
    
    def display_game_over(self, screen: pygame.Surface) -> None:
        screen.blit(self.game_over, self.game_over_rect)
        screen.blit(self.restart, self.restart_rect)
    
    
    def display_score(self, screen: pygame.Surface, score: int) -> None:
        sprites = self.get_score_sprites(score)
        OFFSET = 2
        start = int(SCREEN_WIDTH / 2 - (sum([sprite.get_width() for sprite in sprites]) + (len(sprites) - 1) * OFFSET) / 2)

        cur_offset = 0
        for i, digit in enumerate(sprites):
            screen.blit(digit, (start + cur_offset, 100))
            cur_offset += OFFSET + digit.get_width()
