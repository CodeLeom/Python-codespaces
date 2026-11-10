import csv
import os
import pygame

from ai_actions import choose_simple_action
from game import CoinRush
from game import MAX_STEPS

"""
Min reward: MAX_STEPS * -0.01 - 10 (Max steps reached)
Max reward: 250 - time ???
"""

RESULTS_FILE = "ai_results.csv"

def save_episode_result(steps, finished, total_reward):
    file_exists = os.path.exists(RESULTS_FILE)
    with open(RESULTS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["steps", "finished", "total_reward"])
        writer.writerow([
            steps,
            finished,
            round(total_reward, 2)
        ])

def main():
    pygame.init()

    game = CoinRush()
    state = game.get_state()

    done = False
    step_number = 0

    while not done and game.step_count < MAX_STEPS:
        action = choose_simple_action(state)
        next_state, reward, done = game.step(action)

        state = next_state
        step_number += 1

        if game.step_count % 25 == 0:
            print(
                f"Step: {game.step_count}, "
                f"Action: {action}, "
                f"Reward: {reward:.2f}, "
                f"Coins left: {len(game.coins)} "
                f"Done: {done}"
            )

    print("Episode finished.")
    print(f"Total steps: {game.step_count}")
    print(f"Coins remaining: {len(game.coins)}")
    print(f"Total reward: {game.total_reward:.3f}")
    print(f"Finished: {game.finished}")

    save_episode_result(
        steps=game.step_count,
        finished=game.finished,
        total_reward=game.total_reward
    )

    pygame.quit()


if __name__ == "__main__":
    main()