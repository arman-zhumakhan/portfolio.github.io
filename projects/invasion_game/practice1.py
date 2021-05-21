import pygame
from pygame.sprite import Sprite

class Drop(Sprite):
    """A class represents a single drop"""
    
    def __init__(self, screen, ai_settings):
        """Initialize a drop"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.speed_factor = ai_settings.bullet_speed_factor
    
    
    def update(self, ai_settings):
        """Move the drop down"""
        self.rect.y += ai_settings.bullet_speed_factor
        
    def blitme(self):
        """Draw the alien"""
        self.screen.blit(self.image, self.rect)
    
    