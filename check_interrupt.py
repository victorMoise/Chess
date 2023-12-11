import pygame
import sys

def close_game():
    pygame.quit()
    sys.exit()

def check_user_interrupt(event):
    if event.type == pygame.QUIT:
        close_game()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            close_game()