import pygame
import random
from utils import load_sprite
from models.barrier import Barrier
from collections import deque
from settings import BARRIER_SPAWN_DELAY
from settings import *


class Level:
    def __init__(self) -> None:
        self.bg = load_sprite('assets/sprites/bg.png')
        self.floor = load_sprite('assets/sprites/floor.png')
        self.floor_rect = self.floor.get_rect(x=0, y=800)

        self.barriers: deque[Barrier] = deque()
        self.spawn_ticks = 0

        self.floor_max_offset = self.floor.get_width() - self.bg.get_width()
    
    def restart(self) -> None:
        self.barriers.clear()

    def _remove_hidden_barriers(self) -> None:
        while self.barriers:
            cur_barrier = self.barriers[0]
            if not cur_barrier.is_hidden:
                break
            self.barriers.popleft()
    
    def _spawn_barrier(self, dt: float) -> None:
        self.spawn_ticks += dt
        if self.spawn_ticks > BARRIER_SPAWN_DELAY:
            self.barriers.append(Barrier())
            self.spawn_ticks = 0
    
    def _update_floor_anim(self, dt: float) -> None:
        self.floor_rect.x -= int(BARRIER_SPEED * dt)
        self.floor_rect.x = -(abs(self.floor_rect.x) % self.floor_max_offset)
    
    def get_all_rects(self) -> list[pygame.Rect]:
        rects = [self.floor_rect]
        for barrier in self.barriers:
            rects.append(barrier.down_pipe_rect)
            rects.append(barrier.up_pipe_rect)
        return rects
    
    def update(self, dt: float) -> None:
        self._spawn_barrier(dt)

        for barrier in self.barriers:
            barrier.move(int(BARRIER_SPEED * dt))
        
        self._remove_hidden_barriers()
        self._update_floor_anim(dt)
        

    def display(self, screen: pygame.Surface) -> None:
        screen.blit(self.bg, (0, 0))

        for barrier in self.barriers:
            barrier.display(screen)
        screen.blit(self.floor, self.floor_rect)
