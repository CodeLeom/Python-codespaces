import pygame

from ai_actions import choose_random_action
from game import CoinRush

"""
Min reward: -50
Max reward: 250 - time ???
"""

def main():
    pygame.init()

    game = CoinRush()
    state = game.get_state()

    done = False
    step_number = 0

    while not done and step_number < 5000:
        action = choose_random_action(state)
        next_state, reward, done = game.step(action)

        state = next_state
        step_number += 1

        if step_number % 100 == 0:
            print(
                f"Step: {step_number}, "
                f"Action: {action}, "
                f"Reward: {reward:.2f}, "
                f"Coins left: {len(game.coins)} "
                f"Done: {done}"
            )

    print("Episode finished.")
    print(f"Total steps: {step_number}")
    print(f"Coins remaining: {len(game.coins)}")
    print(f"Total reward: {game.total_reward:.3f}")
    print(f"Finished: {game.finished}")

    pygame.quit()


if __name__ == "__main__":
    main()