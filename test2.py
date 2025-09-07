import pygame
from pygame import display, font, event
from pygame.locals import *

# Setup display
pygame.init()
screen = display.set_mode()
display.set_caption("Capstone 2")
myFont = font.SysFont('arial', 12)  # Choose a font to use in game

# Directions displayed throughout game
directions = "Please press the 'Y' key for yes and the 'N' key for no."

# Counts how many questions have been asked
currentQuestion = 0


# Determines which question to ask
def story(answer, count):
    screen.fill("white")
    if count == 0:
        question1(answer)
    elif count == 1:
        question2(answer)
    elif count == 2:
        question3(answer)
    elif count == 3:
        end(answer)


# Displays the first part of the story
def intro():
    # Break up the string into multiple variables because there isn't text wrapping in Pygame
    intro1 = "Once upon a time lived a brave hero named Anya."
    intro2 = "She lived a simple life in a small village, making biscuits for the village people."
    intro3 = "One day, late at night, she hears a loud noise outside the village."
    q1 = "Should she go outside to investigate? Yes or no?"

    screen.fill("white")
    textSurface = myFont.render(intro1, True, "black")
    screen.blit(textSurface, (10, 10))
    textSurface = myFont.render(intro2, True, "black")
    screen.blit(textSurface, (10, 24))
    textSurface = myFont.render(intro3, True, "black")
    screen.blit(textSurface, (10, 38))
    textSurface = myFont.render(q1, True, "black")
    screen.blit(textSurface, (10, 52))
    textSurface = myFont.render(directions, True, "black")
    screen.blit(textSurface, (10, 66))


# First question
def question1(answer):
    if answer == K_y:
        yes1 = "She ventures into the dark, prepared for danger."
        yes2 = "Eventually, she sees an army of ogres coming toward her village!"
        q2 = "Should she fight the ogres? Yes or no?"

        textSurface = myFont.render(yes1, True, "black")
        screen.blit(textSurface, (10, 10))
        textSurface = myFont.render(yes2, True, "black")
        screen.blit(textSurface, (10, 24))
        textSurface = myFont.render(q2, True, "black")
        screen.blit(textSurface, (10, 38))
        textSurface = myFont.render(directions, True, "black")
        screen.blit(textSurface, (10, 52))

    elif answer == K_n:
        no1 = "She chooses the safety of her home and stays inside."
        no2 = "However, the sounds do not go away."
        no3 = "She can tell something is very wrong..."
        no4 = "Eventually, she sees an army of ogres coming toward her village!"
        q2 = "Should she fight the ogres? Yes or no?"

        textSurface = myFont.render(no1, True, "black")
        screen.blit(textSurface, (10, 10))
        textSurface = myFont.render(no2, True, "black")
        screen.blit(textSurface, (10, 24))
        textSurface = myFont.render(no3, True, "black")
        screen.blit(textSurface, (10, 38))
        textSurface = myFont.render(no4, True, "black")
        screen.blit(textSurface, (10, 52))
        textSurface = myFont.render(q2, True, "black")
        screen.blit(textSurface, (10, 66))
        textSurface = myFont.render(directions, True, "black")
        screen.blit(textSurface, (10, 80))


# Second question
def question2(answer):
    if answer == K_y:
        yes1 = "She bravely confronts the ogres, hoping to protect her village from harm."
        textSurface = myFont.render(yes1, True, "black")
        screen.blit(textSurface, (10, 10))

    elif answer == K_n:
        no1 = "The ogres raid the village but Anya manages to escape with her life."
        textSurface = myFont.render(no1, True, "black")
        screen.blit(textSurface, (10, 10))

    story2 = "The ogres decide to leave but she knows they will be back."
    story3 = "Anya decides to talk with a village elder about what she should do."
    story4 = "The elder says there is a powerful sword hidden in the Ancient Forest."
    q3 = "Should Anya risk her life to retrieve it? Yes or no?"

    textSurface = myFont.render(story2, True, "black")
    screen.blit(textSurface, (10, 24))
    textSurface = myFont.render(story3, True, "black")
    screen.blit(textSurface, (10, 38))
    textSurface = myFont.render(story4, True, "black")
    screen.blit(textSurface, (10, 52))
    textSurface = myFont.render(q3, True, "black")
    screen.blit(textSurface, (10, 66))
    textSurface = myFont.render(directions, True, "black")
    screen.blit(textSurface, (10, 80))


# Third question
def question3(answer):
    if answer == K_y:
        yes1 = "Although Anya almost died in the Ancient Forest,"
        yes2 = "she returns with the Sword of Legends!"
        yes3 = "In the dead of winter, the ogres come back."
        yes4 = "This time they are being led by their evil king."
        q4 = "Should Anya fight the ogre king now that she has the Sword of Legends?"

        textSurface = myFont.render(yes1, True, "black")
        screen.blit(textSurface, (10, 10))
        textSurface = myFont.render(yes2, True, "black")
        screen.blit(textSurface, (10, 24))
        textSurface = myFont.render(yes3, True, "black")
        screen.blit(textSurface, (10, 38))
        textSurface = myFont.render(yes4, True, "black")
        screen.blit(textSurface, (10, 52))
        textSurface = myFont.render(q4, True, "black")
        screen.blit(textSurface, (10, 66))
        textSurface = myFont.render(directions, True, "black")
        screen.blit(textSurface, (10, 80))

    elif answer == K_n:
        no1 = "Anya decides it's too risky to go into the forest alone."
        no2 = "She hopes for the best with the weapons she has."
        no3 = "In the dead of winter, the ogres come back."
        no4 = "This time they are being led by their evil king."
        q4 = "Should Anya fight the king even though she doesn't have the Sword of Legends?"

        textSurface = myFont.render(no1, True, "black")
        screen.blit(textSurface, (10, 10))
        textSurface = myFont.render(no2, True, "black")
        screen.blit(textSurface, (10, 24))
        textSurface = myFont.render(no3, True, "black")
        screen.blit(textSurface, (10, 38))
        textSurface = myFont.render(no4, True, "black")
        screen.blit(textSurface, (10, 52))
        textSurface = myFont.render(q4, True, "black")
        screen.blit(textSurface, (10, 66))
        textSurface = myFont.render(directions, True, "black")
        screen.blit(textSurface, (10, 80))


# Ending
def end(answer):
    if answer == K_y:
        yes1 = "Tension fills the air as she prepares to fight the king. The duel commences..."
        end1 = "After an intense battle, Anya strikes the final blow!"
        end2 = "The king surrenders and pleads for mercy."
        end3 = "Anya is a true hero, who shows mercy to the king."
        end4 = "This act of kindness warms the evil king's heart,"
        end5 = "who promises to leave the village alone for eternity."
        end6 = "The end!"

        textSurface = myFont.render(yes1, True, "black")
        screen.blit(textSurface, (10, 10))
        textSurface = myFont.render(end1, True, "black")
        screen.blit(textSurface, (10, 24))
        textSurface = myFont.render(end2, True, "black")
        screen.blit(textSurface, (10, 38))
        textSurface = myFont.render(end3, True, "black")
        screen.blit(textSurface, (10, 52))
        textSurface = myFont.render(end4, True, "black")
        screen.blit(textSurface, (10, 66))
        textSurface = myFont.render(end5, True, "black")
        screen.blit(textSurface, (10, 80))
        textSurface = myFont.render(end6, True, "black")
        screen.blit(textSurface, (10, 94))

    elif answer == K_n:
        no1 = "Anya refuses to duel the king, who laughs at her cowardice."
        end1 = "This buys some time for the villagers to escape."
        end2 = "Sadly, the ogre king takes over Anya's village."
        end3 = "She is just thankful that the villagers were able to get to safety."
        end4 = "The end!"

        textSurface = myFont.render(no1, True, "black")
        screen.blit(textSurface, (10, 10))
        textSurface = myFont.render(end1, True, "black")
        screen.blit(textSurface, (10, 24))
        textSurface = myFont.render(end2, True, "black")
        screen.blit(textSurface, (10, 38))
        textSurface = myFont.render(end3, True, "black")
        screen.blit(textSurface, (10, 52))
        textSurface = myFont.render(end4, True, "black")
        screen.blit(textSurface, (10, 66))


# Game loop
while True:
    # Checks to see if at beginning of game
    if currentQuestion == 0:
        intro()

    # Get the most recent event
    currentEvent = event.poll()

    # Displays the correct question based on event that occurs
    if currentEvent.type == KEYDOWN:
        story(currentEvent.key, currentQuestion)
        currentQuestion = currentQuestion + 1

    # add text to screen
    display.update()