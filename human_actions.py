import pygame

def get_keyboard_action():
    keys = pygame.key.get_pressed()
    """
        Actions:
        0 = no movement
        1 = up
        2 = down
        3 = left
        4 = right
    """
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        return 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        return 2
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        return 3
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        return 4
    return 0