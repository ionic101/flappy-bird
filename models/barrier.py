import pygame
import random
from utils import load_sprite
from settings import *


class Barrier:
    def __init__(self) -> None:
        self.down_pipe = load_sprite('assets/sprites/pipe.png')
        self.up_pipe = pygame.transform.flip(self.down_pipe, False, True)
        self.x: float = SCREEN_WIDTH
        self.y: float = -self._get_random_y()

        self._down_pipe_rect = self.down_pipe.get_rect(x=self.x, y=self.y)
        self._up_pipe_rect = self.up_pipe.get_rect(x=self.x, y=self.y)

        self.is_passed = False
    
    @property
    def center_x(self) -> int:
        return int(self.x + self._down_pipe_rect.x)

    @property
    def down_pipe_rect(self) -> pygame.Rect:
        self._down_pipe_rect.x = int(self.x)
        self._down_pipe_rect.y = int(self.y + self.down_pipe.get_height() + HOLE_SIZE)
        return self._down_pipe_rect

    @property
    def up_pipe_rect(self) -> pygame.Rect:
        self._up_pipe_rect.x = int(self.x)
        self._up_pipe_rect.y = int(self.y)
        return self._up_pipe_rect

    @property
    def is_hidden(self) -> bool:
        return self.x < -self.down_pipe.get_width()
    
    def _get_random_y(self) -> int:
        return random.randint(*HOLE_RANGE)

    def move(self, dx: float) -> None:
        self.x -= dx
    
    def _display_collision(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, 'red', self.up_pipe_rect, COLLISION_WIDTH)
        pygame.draw.rect(screen, 'red', self.down_pipe_rect, COLLISION_WIDTH)

    def display(self, screen: pygame.Surface) -> None:
        screen.blit(self.up_pipe, self.up_pipe_rect)
        screen.blit(self.down_pipe, self.down_pipe_rect)
        self._display_collision(screen)
