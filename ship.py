import pygame


class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        """Initializes the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load(self.settings.ship_image)
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self, dt):
        """Update the ship's position based on the movement flag"""
        # ---------- Right and Left Movement ----------
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_x * dt
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed_x * dt
        # ---------- Up and Down Movement ----------
        if self.moving_up and self.rect.top > self.settings.screen_height * 0.60: # Only move up to 40% of the screen
            self.y += self.settings.ship_speed_y * dt
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y -= self.settings.ship_speed_y * dt

        # Update rect object from self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
