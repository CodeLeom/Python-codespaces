import random
import sys
import time

import pygame


WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 260
COIN_COUNT = 15

BACKGROUND = (35, 40, 50)
PLAYER_COLOR = (70, 170, 255)
COIN_COLOR = (245, 205, 45)
FINISH_LOCKED = (110, 110, 110)
FINISH_OPEN = (70, 200, 100)
WHITE = (245, 245, 245)


class CoinRush:
    def __init__(self):
        self.player = pygame.Rect(55, HEIGHT // 2 - 16, 32, 32)
        self.finish = pygame.Rect(WIDTH - 100, HEIGHT // 2 - 55, 55, 110)
        self.coins = self.create_coins()
        self.start_time = time.perf_counter()
        self.finish_time = None
        self.finished = False

    def create_coins(self):
        coins = []
        while len(coins) < COIN_COUNT:
            coin = pygame.Rect(
                random.randint(120, WIDTH - 170),
                random.randint(50, HEIGHT - 70),
                18,
                18,
            )
            if coin.colliderect(self.player.inflate(80, 80)):
                continue
            if coin.colliderect(self.finish.inflate(50, 20)):
                continue
            if any(coin.colliderect(other.inflate(25, 25)) for other in coins):
                continue
            coins.append(coin)
        return coins

    def reset(self):
        self.__init__()

    def get_state(self):
        player_x = self.player.x / WIDTH
        player_y = self.player.y / HEIGHT

        finish_x = self.finish.x / WIDTH
        finish_y = self.finish.y / HEIGHT

        if self.coins:
            nearest_coin = min(
                self.coins,
                key=lambda coin: self.player.center.distance_to(coin.center),
            )

            coin_x = nearest_coin.centerx / WIDTH
            coin_y = nearest_coin.centery / HEIGHT
        else:
            coin_x = 0
            coin_y = 0

        coins_remaining = len(self.coins) / COIN_COUNT

        return [
            player_x,
            player_y,
            coin_x,
            coin_y,
            finish_x,
            finish_y,
            coins_remaining,
        ]

    def get_direction_from_action(self, action):
        """
    Convert an action number into a movement direction.

    Actions:
        0 = no movement
        1 = up
        2 = down
        3 = left
        4 = right
        """
        directions = {
            0: pygame.Vector2(0, 0),   # Stay still
            1: pygame.Vector2(0, -1),  # Move upward
            2: pygame.Vector2(0, 1),   # Move downward
            3: pygame.Vector2(-1, 0),  # Move left
            4: pygame.Vector2(1, 0),   # Move right
        }

        return directions.get(action, pygame.Vector2(0, 0))  # Default to no movement

    def update(self, dt, action=None):
        if self.finished:
            return
        if action is None:
            # Normal gameplay
            keys = pygame.key.get_pressed()
            direction = pygame.Vector2(
                keys[pygame.K_d] - keys[pygame.K_a],
                keys[pygame.K_s] - keys[pygame.K_w],
            )
        else:
            direction = self.get_direction_from_action(action)
        
        if direction.length_squared():
            direction = direction.normalize()

        self.player.x += round(direction.x * PLAYER_SPEED * dt)
        self.player.y += round(direction.y * PLAYER_SPEED * dt)
        self.player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        self.coins = [coin for coin in self.coins if not self.player.colliderect(coin)]

        if not self.coins and self.player.colliderect(self.finish):
            self.finish_time = time.perf_counter() - self.start_time
            self.finished = True

    def step(self, action):
        """
        Advance the game by one fixed simulation step.

        The AI gives us an action number. We update the game,
        then return information about what happened.
        """
        # A fixed timestep makes training predictable.
        dt = 1 / FPS

        coins_before = len(self.coins)

        # Send the action to the movement system.
        self.update(dt, action)

        coins_collected = coins_before - len(self.coins)

        # Small penalty for taking time.
        reward = -0.01

        # Reward the AI for collecting coins.
        reward += coins_collected * 10

        # Check whether the player finished.
        done = False

        if not self.coins and self.player.colliderect(self.finish):
            reward += 100
            done = True

        return self.get_state(), reward, done

    def draw(self, screen, font, big_font):
        screen.fill(BACKGROUND)

        finish_color = FINISH_OPEN if not self.coins else FINISH_LOCKED
        pygame.draw.rect(screen, finish_color, self.finish, border_radius=8)
        finish_text = "FINISH" if not self.coins else "LOCKED"
        text = font.render(finish_text, True, (10, 30, 15) if not self.coins else WHITE)
        screen.blit(text, text.get_rect(center=self.finish.center))

        for coin in self.coins:
            pygame.draw.circle(screen, COIN_COLOR, coin.center, 10)
            pygame.draw.circle(screen, (255, 240, 130), coin.center, 5, 2)

        pygame.draw.rect(screen, PLAYER_COLOR, self.player, border_radius=6)
        pygame.draw.circle(screen, WHITE, self.player.center, 5)

        elapsed = self.finish_time if self.finished else time.perf_counter() - self.start_time
        hud = font.render(
            f"Coins: {COIN_COUNT - len(self.coins)}/{COIN_COUNT}    Time: {elapsed:.2f}s",
            True,
            WHITE,
        )
        screen.blit(hud, (20, 20))
        instructions = font.render("WASD / arrows: move    Collect all coins, then reach FINISH", True, WHITE)
        screen.blit(instructions, (20, HEIGHT - 38))

        if self.finished:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 165))
            screen.blit(overlay, (0, 0))
            title = big_font.render("FINISHED!", True, WHITE)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 35)))
            result = font.render(
                f"Your time: {self.finish_time:.2f}s    Press R to try again",
                True,
                WHITE,
            )
            screen.blit(result, result.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 35)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Coin Rush")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    big_font = pygame.font.SysFont("arial", 52, bold=True)
    game = CoinRush()

    while True:
        dt = min(clock.tick(FPS) / 1000, 0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    game.reset()

        game.update(dt)
        game.draw(screen, font, big_font)
        pygame.display.flip()


if __name__ == "__main__":
    main()
