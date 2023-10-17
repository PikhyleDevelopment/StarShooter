class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""
        # ------------ Screen settings ------------
        self.full_screen = False
        # Screen width and height if self.full_screen is False.
        # Otherwise, these settings are ignored. See alien_invasion.__init__()
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0, 0, 0)
        self.bg_image = 'images/SpaceShooterRedux/Backgrounds/darkPurple.png'

        # ------------ Ship settings ------------
        self.ship_image = 'images/SpaceShooterRedux/PNG/playerShip1_blue.png'
        self.ship_speed = 2.5

        # ------------ Bullet settings ------------
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (0, 255, 0)
        self.bullet_image = 'images/SpaceShooterRedux/PNG/Lasers/laserGreen10.png'
        self.bullet_inventory = 5

        # ------------ Super bullet settings ------------
        self.super_bullet_speed = 4.0
        self.super_bullet_width = 60
        self.super_bullet_height = 15
        self.super_bullet_image = 'images/SpaceShooterRedux/PNG/Lasers/laserRed14.png'
        self.super_bullet_inventory = 10

        # ------------ Alien settings ------------
        self.alien_image = 'images/SpaceShooterRedux/PNG/Enemies/enemyRed3.png'
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # ------------ Effects settings ------------
        self.star1 = 'images/SpaceShooterRedux/PNG/Effects/star1.png'
        self.star2 = 'images/SpaceShooterRedux/PNG/Effects/star2.png'
        self.star3 = 'images/SpaceShooterRedux/PNG/Effects/star3.png'
