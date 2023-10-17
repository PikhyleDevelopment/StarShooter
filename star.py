from random import randint

import pygame.image
from pygame.sprite import Sprite


class Star(Sprite):
    """A class to manage background stars"""

    def __init__(self, ai_game):
        """Initializes a star and sets its location"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        random_int = randint(1, 3)
        match random_int:
            case 1:
                self.image = pygame.image.load(self.settings.star1)
            case 2:
                self.image = pygame.image.load(self.settings.star2)
            case 3:
                self.image = pygame.image.load(self.settings.star3)

        self.rect = self.image.get_rect()

        # Start a star in a random location on the screen
        random_x = randint(0, self.settings.screen_width)
        random_y = randint(0, self.settings.screen_height)
        self.rect.x = random_x
        self.rect.y = random_y

        # Store the star's exact horizontal and vertical positions
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
