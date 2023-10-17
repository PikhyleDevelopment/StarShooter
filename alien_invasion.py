import sys
from random import randint

import pygame

from alien import Alien
from bullet import Bullet, SuperBullet
from settings import Settings
from ship import Ship
from star import Star


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initializes the game, and create game resources"""
        pygame.init()
        # Load in our settings
        self.settings = Settings()
        # Determine and set screen settings
        if self.settings.full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
            self.settings.ship_speed_x = 2
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height)
            )
        # Initialize our game objects
        self.stars = pygame.sprite.Group()
        self._gen_starfield()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.super_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Set window caption and background
        pygame.display.set_caption("Alien Invasion")
        # self.bg_color = self.settings.bg_color
        # self.bg_image = pygame.image.load(self.settings.bg_image)
        # self.bg_image = pygame.transform.scale(
        #     self.bg_image,
        #     (
        #         self.settings.screen_width,
        #         self.settings.screen_height
        #     )
        # )

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # Watch for keyboard and mouse events
            self._check_events()
            # Update the ship
            self.ship.update()
            # Update the bullets
            self._update_bullets()
            self._update_super_bullets()
            # Update the aliens
            self._update_aliens()
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
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        if event.key == pygame.K_KP0:
            self._fire_super_bullet()
        if event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullet_inventory:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Update images on the screen and flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        # self.screen.blit(self.bg_image, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.blitme()
        for super_bullet in self.super_bullets.sprites():
            super_bullet.blitme()

        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions();

    def _check_bullet_alien_collisions(self):
        # Check for any bullets that have hit aliens
        # if so, get rid of the bullet and the alien
        bullet_collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()

    def _update_super_bullets(self):
        self.super_bullets.update()
        for super_bullet in self.super_bullets.copy():
            if super_bullet.rect.bottom <= 0:
                self.super_bullets.remove(super_bullet)

        self._check_super_bullet_alien_collisions()

    def _check_super_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.super_bullets, self.aliens, True, True
        )

        if not self.aliens:
            self.super_bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that can fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _gen_starfield(self):
        """Generates a starfield on the background."""
        # Create a random number of stars and add them to self.stars group
        for num in range(20, randint(30, 40)):
            star = Star(self)
            self.stars.add(star)

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
            then update the positions of all aliens in the fleet
        :return: None
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien - player ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!")

    def _fire_super_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.super_bullets) < self.settings.super_bullet_inventory:
            new_super_bullet = SuperBullet(self)
            self.super_bullets.add(new_super_bullet)


if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
