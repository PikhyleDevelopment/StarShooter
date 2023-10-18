import sys
from random import randint
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet, SuperBullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from star import Star


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initializes the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        # ------------ Time Settings ------------
        self.TARGET_FPS = 60
        self.clock = pygame.time.Clock()
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
        pygame.display.set_caption("Alien Invasion")
        # Initialize our game objects
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.stars = pygame.sprite.Group()
        self._gen_starfield()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.super_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        # Load in our settings


        self._create_fleet()

        # Make a play button
        self.play_button = Button(self, "Play")

        # --------------- Background image settings ---------------- #
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
            if self.stats.game_active:
                self.dt = self.clock.tick(60) * .001 * self.TARGET_FPS
                # Update the ship
                self.ship.update(self.dt)
                # Update the bullets
                self._update_bullets(self.dt)
                self._update_super_bullets(self.dt)
                # Update the aliens
                self._update_aliens(self.dt)
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset game settings
            self.settings.initialize_dynamic_settings()
            # Reset the game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()

            self._reset_entities()
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

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

        # Draw the score information
        self.sb.show_score()

        # Draw play button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _update_bullets(self, dt):
        self.bullets.update(dt)
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
        if bullet_collisions:
            for aliens in bullet_collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self._reset_entities()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_super_bullets(self, dt):
        self.super_bullets.update(dt)
        for super_bullet in self.super_bullets.copy():
            if super_bullet.rect.bottom <= 0:
                self.super_bullets.remove(super_bullet)

        self._check_super_bullet_alien_collisions()

    def _check_super_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.super_bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self._reset_entities()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

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

    def _update_aliens(self, dt):
        """
        Check if the fleet is at an edge,
            then update the positions of all aliens in the fleet
        :return: None
        """
        self._check_fleet_edges()
        self.aliens.update(dt)

        # Look for alien - player ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check to see if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as the alien hitting the player ship
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1

            self._reset_entities()
            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _fire_super_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.super_bullets) < self.settings.super_bullet_inventory:
            new_super_bullet = SuperBullet(self)
            self.super_bullets.add(new_super_bullet)

    def _reset_entities(self):
        # Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()
        self.super_bullets.empty()
        if self.settings.DEBUG:
            print(f"""
============================ DEBUG: Entity Speeds ============================
                       Ship X Speed : {self.settings.ship_speed_x}
                       Ship Y Speed : {self.settings.ship_speed_y}
                       Bullet Speed : {self.settings.bullet_speed}
                 Super Bullet Speed : {self.settings.super_bullet_speed}
                        Alien Speed : {self.settings.alien_speed}
                    """)

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()


if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
