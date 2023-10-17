import sys

import pygame

from bullet import Bullet
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initializes the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.bullets = pygame.sprite.Group()

        if self.settings.full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
            self.settings.ship_speed = 2
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height)
            )
        self.ship = Ship(self)
        pygame.display.set_caption("Alien Invasion")
        self.bg_image = pygame.image.load(self.settings.bg_image)
        self.bg_image = pygame.transform.scale(
            self.bg_image,
            (
                self.settings.screen_width,
                self.settings.screen_height
            )
        )

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # Watch for keyboard and mouse events
            self._check_events()
            # Update the ship
            self.ship.update()
            # Update the bullets
            self._update_bullets()
            # Redraw the screen during each pass through the loop
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            # Move the ship to the right
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        if event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullet_inventory:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Update images on the screen and flip to new screen"""
        # self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.bg_image, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
