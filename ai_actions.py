import random

ACTION_COUNT = 9

def choose_random_action(state):
    """
    Choose a random movement action.

    This is not intelligent yet. It is only a temporary AI
    used to test whether the game can be controlled without
    keyboard input.

    The state parameter will eventually be used by a trained AI.
    """
    del state

    # randint includes both endpoints, so this returns 0 through 8.
    return random.randint(0, ACTION_COUNT - 1)