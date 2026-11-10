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

def choose_simple_action(state):
    """
    Choose movement based on the current game state.

    State indexes:
        2 = horizontal direction to nearest coin
        3 = vertical direction to nearest coin
        4 = horizontal direction to finish
        5 = vertical direction to finish
        6 = percentage of coins remaining
    """
    coin_dx = state[2]
    coin_dy = state[3]
    finish_dx = state[4]
    finish_dy = state[5]
    coins_remaining = state[6]

    if coins_remaining > 0:
        target_dx = coin_dx
        target_dy = coin_dy
    else:
        target_dx = finish_dx
        target_dy = finish_dy

    # Convert the target direction into an action number.
    horizontal = 0
    vertical = 0

    # A small threshold prevents jitter when nearly aligned.
    threshold = 0.005
    """
    if target_dx > threshold:
        horizontal = 1
    elif target_dx < -threshold:
        horizontal = -1

    if target_dy > threshold:
        vertical = 1
    elif target_dy > -threshold:
        vertical = -1
    """

    if abs(target_dx) < threshold and abs(target_dy) < threshold:
        # The AI is close enough to stop.
        horizontal = 0
        vertical = 0
    elif abs(target_dx) > abs(target_dy):
        # Move horizontally when the horizontal gap is larger.
        horizontal = 1 if target_dx > 0 else -1
        vertical = 0
    else:
        # Move vertically when the vertical gap is larger.
        horizontal = 0
        vertical = 1 if target_dy > 0 else -1

    directions = {
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

    return directions[(horizontal, vertical)]