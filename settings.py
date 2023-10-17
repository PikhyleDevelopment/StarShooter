class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""
        # Screen settings
        self.full_screen = False
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (32, 32, 32)
        self.bg_image = 'images/SpaceShooterRedux/Backgrounds/darkPurple.png'

        # Ship settings
        self.ship_image = 'images/SpaceShooterRedux/PNG/playerShip1_blue.png'
        self.ship_speed = 1.5