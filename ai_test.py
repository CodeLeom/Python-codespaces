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

EPISODES = 10
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
    for episode in range(EPISODES):
        game = CoinRush()
        state = game.get_state()

        done = False

        while not done and game.step_count < MAX_STEPS:
            action = choose_simple_action(state)
            next_state, reward, done = game.step(action)

            state = next_state

        save_episode_result(
            steps=game.step_count,
            finished=game.finished,
            total_reward=game.total_reward
        )

        print(
            f"Episode {episode + 1}: "
            f"Total steps: {game.step_count}, "
            f"Total reward: {game.total_reward:.3f}, "
            f"Finished: {game.finished}, "
        )

    pygame.quit()


if __name__ == "__main__":
    main()