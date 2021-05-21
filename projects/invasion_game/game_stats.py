import json

class GameStats():
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # Start the game in active state
        self.game_active = False
        
        self.filename = 'high_score.json'
        
        # High score should never be reset
        self.initialize_high_score()
        
    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ship_lift = self.ai_settings.ship_lift
        self.score = 0
        self.level = 1
    
    
    def initialize_high_score(self):
        """Initialize the highest score from the file"""
        try:
            with open(self.filename) as obj:
                self.high_score = json.load(obj)
        except FileNotFoundError:
            self.high_score = 0
            with open(self.filename, 'w') as obj:
                json.dump(self.high_score, obj)
    