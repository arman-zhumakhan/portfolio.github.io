class Settings():
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize the game's settings."""
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (230, 230, 230)
        self.ship_lift = 3
        
        # Bullet settigns
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 10
        
        # Alien
        self.fleet_drop_speed = 10
        
        # How quickly the game speeds up
        self.speedup_scale = 1.5
        
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    
    def initialize_dynamic_settings(self):
        """Initialize the settings that change throughout the game"""
        self.ship_speed_factor = 7
        self.bullet_speed_factor = 7
        self.alien_speed_factor = 7
        
        # 1 represens right; -1 represents left
        self.fleet_direction = 1
        self.alien_points = 50
        
    
    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)