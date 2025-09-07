import pygame
from pygame import draw, display

# Set up pygame window
pygame.init()
window = display.set_mode((600, 600))
display.set_caption("A Very Big House")
window.fill("cyan")

# set up objects

background = pygame.Rect(0, 220, 600, 400)
house = pygame.Rect(90, 180, 300, 400)
door = pygame.Rect(190, 215, 100, 140)
window1 = pygame.Rect(110, 215, 60, 60)
window2 = pygame.Rect(310, 215, 60, 60)
window1_1 = pygame.Rect(110, 215, 30, 60)
window1_2 = pygame.Rect(310, 215, 30, 60)
doorKnob = pygame.Rect(265, 284, 15, 5)
roof = pygame.Rect(80, 140, 320, 50)

#draw house objects

draw.rect(window, "green", background)
draw.rect(window, "white", house)
draw.rect(window, "orangered", door)
draw.rect(window, "blue", window1)
draw.rect(window, "blue", window2)
draw.rect(window, "dark grey", doorKnob)
draw.rect(window, "grey", window1_1)
draw.rect(window, "grey", window1_2)
draw.rect(window, "brown", roof)
display.flip()

#update display
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # ✅ handles close button
            running = False

pygame.quit()