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

    def update(self, dt):
        if self.finished:
            return

        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w],
        )
        if direction.length_squared():
            direction = direction.normalize()

        self.player.x += round(direction.x * PLAYER_SPEED * dt)
        self.player.y += round(direction.y * PLAYER_SPEED * dt)
        self.player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        self.coins = [coin for coin in self.coins if not self.player.colliderect(coin)]

        if not self.coins and self.player.colliderect(self.finish):
            self.finish_time = time.perf_counter() - self.start_time
            self.finished = True

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
