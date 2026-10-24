from pygame.image import load
from pygame.transform import scale2x
from pygame import Surface


def load_sprite(path: str) -> Surface:
    return scale2x(load(path))
