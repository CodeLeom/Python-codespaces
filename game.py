import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() // 2, screen.get_height() // 2) # Start player in the center of the screen

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Fill the screen with black

    pygame.draw.circle(screen, "red", player_pos, 20)  # Draw the player as a red circle    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos.x -= 200 * dt  # Move left
    if keys[pygame.K_RIGHT]:
        player_pos.x += 200 * dt  # Move right
    if keys[pygame.K_UP]:
        player_pos.y -= 200 * dt  # Move up
    if keys[pygame.K_DOWN]:
        player_pos.y += 200 * dt  # Move down

    pygame.display.flip()  # Update the display

    dt = clock.tick(60) / 1000  # Calculate the time passed since the last frame

pygame.quit()