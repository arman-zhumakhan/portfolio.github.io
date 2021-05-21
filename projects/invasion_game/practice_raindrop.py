import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from practice1 import Drop

def check_events():
    """Respond to actions of users"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()


def update_drop(drops, ai_settings):
    """Update the positions of drops"""
    drops.update(ai_settings)
    
    for drop in drops.copy():
        if drop.rect.bottom >= ai_settings.screen_height:
            drop.rect.bottom = 0
            


def update_screen(ai_settings, screen, drops):
    screen.fill(ai_settings.bg_color)
    for drop in drops.sprites():
        drop.blitme()
    
    pygame.display.flip() 
    
    
    
def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
            (ai_settings.screen_width , ai_settings.screen_height))
    pygame.display.set_caption("Aline Invasion")
    ai_settings = Settings()
    drops = Group()
    
    drop = Drop(screen, ai_settings)
    available_space_x = ai_settings.screen_width - 2*drop.rect.width
    number_x = int(available_space_x / (2*drop.rect.width))
    number_y = int((ai_settings.screen_height-2*drop.rect.height)/drop.rect.height)
    
    for row in range(number_y):
        for column in range(number_x):
            drop = Drop(screen, ai_settings)
            drop.rect.x = drop.rect.width + 2 * column * drop.rect.width
            drop.rect.y = drop.rect.height + 2 * row * drop.rect.height
            drops.add(drop)
            
    while True:
        check_events()
        update_drop(drops,ai_settings)
        update_screen(ai_settings, screen, drops)
    
    
run_game()