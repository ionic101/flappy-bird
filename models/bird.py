import pygame
from utils import load_sprite
from settings import *


class Bird:
    def __init__(self) -> None:
        self.x: float = BIRD_START_X
        self.y: float = BIRD_START_Y
        self.speed = 0

        self.anim_sprites = [
            load_sprite('assets/sprites/bird/bird_down.png'),
            load_sprite('assets/sprites/bird/bird_middle.png'),
            load_sprite('assets/sprites/bird/bird_up.png'),
            load_sprite('assets/sprites/bird/bird_middle.png'),
        ]

        self.anim_ticks = 0
        self._rect = pygame.Rect(self.x, self.y, BIRD_COLLISION_WIDTH, BIRD_COLLITION_HEIGHT)
    
    def restart(self) -> None:
        self.x = BIRD_START_X
        self.y = BIRD_START_Y
        self.speed = 0
    
    @property
    def rect(self) -> pygame.Rect:
        self._rect.center = (int(self.x), int(self.y))
        return self._rect

    @property
    def angle(self) -> float:
        if self.speed < 0:
            return MAX_UP_ANGLE * (-self.speed / JUMP_IMPULSE)
        else:
            return MAX_DOWN_ANGLE * (self.speed / GRAVITATION)
    
    def _update_gravity(self, dt: float) -> None:
        if self.speed + GRAVITATION * dt < GRAVITATION:
            self.speed += GRAVITATION * dt
    
    def _get_anim_sprite(self, dt: float) -> pygame.Surface:
        self.anim_ticks += dt
        if self.anim_ticks > BIRD_ANIM_DELAY * len(self.anim_sprites):
            self.anim_ticks = 0
        return self.anim_sprites[int(self.anim_ticks / BIRD_ANIM_DELAY)]
    
    def jump(self) -> None:
        self.speed = -JUMP_IMPULSE

    def update(self, dt: float) -> None:
        self._update_gravity(dt)
        self.y += int(self.speed * dt)
        if self.y < MAX_Y:
            self.y = MAX_Y
    
    def display(self, screen: pygame.Surface, dt: float) -> None:
        sprite = self._get_anim_sprite(dt)
        rotated_sprite = pygame.transform.rotate(sprite, self.angle)
        display_rect = rotated_sprite.get_rect(center=(self.x, self.y))
        
        screen.blit(rotated_sprite, display_rect)
        pygame.draw.rect(screen, 'red', self.rect, COLLISION_WIDTH)
