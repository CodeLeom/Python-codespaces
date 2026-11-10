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
        5 = up-left
        6 = up-right
        7 = down-left
        8 = down-right
    """
    left = bool(keys[pygame.K_a] or keys[pygame.K_LEFT])
    right = bool(keys[pygame.K_d] or keys[pygame.K_RIGHT])
    up = bool(keys[pygame.K_w] or keys[pygame.K_UP])
    down = bool(keys[pygame.K_s] or keys[pygame.K_DOWN])

    direction = (
        int(right) - int(left),
        int(down) - int(up),
    )

    actions = {        
        (0, 0): 0,
        (0, -1): 1,
        (0, 1): 2,
        (-1, 0): 3,
        (1, 0): 4,
        (-1, -1): 5,
        (1, -1): 6,
        (-1, 1): 7,
        (1, 1): 8,
    }

    return actions.get(direction)