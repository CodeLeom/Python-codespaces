import math
import random
import sys

import pygame


# A small, asset-free stealth game prototype.
WIDTH, HEIGHT = 1000, 700
FPS = 60
PLAYER_SIZE = 24
PLAYER_SPEED = 230
GUARD_SPEED = 110
DETECTION_DISTANCE = 230
DETECTION_ANGLE = 55

BG = (35, 38, 45)
FLOOR = (55, 59, 68)
WALL = (25, 27, 32)
WHITE = (235, 235, 235)
MONEY = (245, 205, 55)
PLAYER_COLOR = (70, 180, 255)
GUARD_COLOR = (225, 75, 75)
PUDDLE_COLOR = (45, 105, 150)
EXIT_COLOR = (80, 190, 100)


class Player:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        self.rect.center = self.pos
        self.money = 0
        self.base_speed = PLAYER_SPEED

    def update(self, dt, puddles, walls):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w],
        )
        if direction.length_squared():
            direction = direction.normalize()

        speed = self.base_speed
        if any(puddle.colliderect(self.rect) for puddle in puddles):
            speed *= 0.42

        self.move_axis(direction.x * speed * dt, 0, walls)
        self.move_axis(0, direction.y * speed * dt, walls)

    def move_axis(self, dx, dy, walls):
        self.pos.x += dx
        self.rect.centerx = round(self.pos.x)
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right
                self.pos.x = self.rect.centerx

        self.pos.y += dy
        self.rect.centery = round(self.pos.y)
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                elif dy < 0:
                    self.rect.top = wall.bottom
                self.pos.y = self.rect.centery

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
        self.pos = pygame.Vector2(self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect, border_radius=5)
        pygame.draw.circle(surface, WHITE, self.rect.center, 4)


class Guard:
    def __init__(self, patrol_points):
        self.points = [pygame.Vector2(point) for point in patrol_points]
        self.position = self.points[0].copy()
        self.target_index = 1
        self.facing = pygame.Vector2(1, 0)
        self.alert = 0.0

    def update(self, dt):
        target = self.points[self.target_index]
        offset = target - self.position
        if offset.length() < 4:
            self.target_index = (self.target_index + 1) % len(self.points)
            return
        self.facing = offset.normalize()
        self.position += self.facing * GUARD_SPEED * dt

    def can_see(self, player, walls):
        to_player = player.pos - self.position
        distance = to_player.length()
        if distance > DETECTION_DISTANCE or distance == 0:
            return False

        angle = math.degrees(self.facing.angle_to(to_player))
        if abs(angle) > DETECTION_ANGLE / 2:
            return False

        sight_line = pygame.Vector2(self.position)
        for _ in range(max(1, int(distance / 8))):
            sight_line += to_player.normalize() * 8
            if any(wall.collidepoint(sight_line) for wall in walls):
                return False
        return True

    def draw(self, surface):
        end = self.position + self.facing * DETECTION_DISTANCE
        cone = [
            self.position,
            self.position + self.facing.rotate(DETECTION_ANGLE / 2) * DETECTION_DISTANCE,
            self.position + self.facing.rotate(-DETECTION_ANGLE / 2) * DETECTION_DISTANCE,
        ]
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(overlay, (255, 220, 80, 28), cone)
        surface.blit(overlay, (0, 0))
        pygame.draw.line(surface, (245, 190, 70), self.position, end, 2)
        pygame.draw.circle(surface, GUARD_COLOR, self.position, 16)
        pygame.draw.circle(surface, WHITE, self.position, 4)


def make_money():
    return [
        pygame.Rect(115, 115, 18, 18),
        pygame.Rect(270, 100, 18, 18),
        pygame.Rect(470, 160, 18, 18),
        pygame.Rect(760, 115, 18, 18),
        pygame.Rect(870, 300, 18, 18),
        pygame.Rect(620, 480, 18, 18),
        pygame.Rect(350, 560, 18, 18),
        pygame.Rect(125, 470, 18, 18),
        pygame.Rect(780, 585, 18, 18),
        pygame.Rect(520, 360, 18, 18),
    ]


def make_level():
    walls = [
        pygame.Rect(0, 0, WIDTH, 18),
        pygame.Rect(0, HEIGHT - 18, WIDTH, 18),
        pygame.Rect(0, 0, 18, HEIGHT),
        pygame.Rect(WIDTH - 18, 0, 18, HEIGHT),
        pygame.Rect(190, 70, 28, 230),
        pygame.Rect(190, 390, 28, 220),
        pygame.Rect(390, 70, 28, 190),
        pygame.Rect(390, 340, 28, 270),
        pygame.Rect(600, 70, 28, 220),
        pygame.Rect(600, 380, 28, 230),
        pygame.Rect(805, 70, 28, 170),
        pygame.Rect(805, 330, 28, 280),
        pygame.Rect(70, 315, 120, 26),
        pygame.Rect(220, 315, 170, 26),
        pygame.Rect(420, 315, 180, 26),
        pygame.Rect(630, 315, 175, 26),
    ]
    puddles = [
        pygame.Rect(65, 110, 75, 50),
        pygame.Rect(255, 410, 105, 60),
        pygame.Rect(450, 105, 85, 55),
        pygame.Rect(680, 420, 100, 65),
        pygame.Rect(850, 500, 85, 45),
    ]
    guards = [
        Guard([(80, 220), (170, 220), (170, 570), (80, 570)]),
        Guard([(260, 100), (350, 100), (350, 270), (260, 270)]),
        Guard([(470, 410), (570, 410), (570, 570), (470, 570)]),
        Guard([(690, 110), (770, 110), (770, 270), (690, 270)]),
    ]
    return walls, puddles, guards


def draw_text(surface, font, message, position, color=WHITE):
    surface.blit(font.render(message, True, color), position)


def draw_game(surface, player, walls, puddles, money, guards, exit_rect, font, state):
    surface.fill(BG)
    pygame.draw.rect(surface, FLOOR, (18, 18, WIDTH - 36, HEIGHT - 36))

    for puddle in puddles:
        pygame.draw.ellipse(surface, PUDDLE_COLOR, puddle)
        pygame.draw.ellipse(surface, (80, 145, 190), puddle, 2)

    for wall in walls:
        pygame.draw.rect(surface, WALL, wall)

    pygame.draw.rect(surface, EXIT_COLOR, exit_rect, border_radius=4)
    draw_text(surface, font, "EXIT", (exit_rect.x + 8, exit_rect.y + 13), (10, 40, 15))

    for bill in money:
        pygame.draw.rect(surface, MONEY, bill, border_radius=3)
        pygame.draw.line(surface, (130, 95, 20), bill.center, (bill.centerx, bill.top + 4), 2)

    for guard in guards:
        guard.draw(surface)
    player.draw(surface)

    pygame.draw.rect(surface, (20, 22, 27), (18, 18, WIDTH - 36, 45))
    draw_text(surface, font, f"Cash: ${player.money}   Bags left: {len(money)}", (32, 30))
    draw_text(surface, font, "WASD / arrows: move    Collect cash, then reach the green exit", (390, 30), (195, 205, 215))

    if state != "playing":
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 170))
        surface.blit(shade, (0, 0))
        title = "CAUGHT!" if state == "caught" else "YOU GOT AWAY!"
        subtitle = "Press R to try again or Esc to quit"
        title_surface = pygame.font.SysFont("arial", 52, bold=True).render(title, True, WHITE)
        surface.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 35)))
        draw_text(surface, font, subtitle, (WIDTH // 2 - 150, HEIGHT // 2 + 25), WHITE)


def new_game():
    walls, puddles, guards = make_level()
    return Player((75, 75)), walls, puddles, make_money(), guards, pygame.Rect(900, 70, 75, 55), "playing"


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Night Shift: A Small Robbery Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 18)
    player, walls, puddles, money, guards, exit_rect, state = new_game()

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
                if event.key == pygame.K_r and state != "playing":
                    player, walls, puddles, money, guards, exit_rect, state = new_game()

        if state == "playing":
            player.update(dt, puddles, walls)
            for guard in guards:
                guard.update(dt)

            money = [bill for bill in money if not player.rect.colliderect(bill)]
            player.money = (10 - len(money)) * 100

            if any(guard.can_see(player, walls) for guard in guards):
                state = "caught"
            elif not money and player.rect.colliderect(exit_rect):
                state = "escaped"

        draw_game(screen, player, walls, puddles, money, guards, exit_rect, font, state)
        pygame.display.flip()


if __name__ == "__main__":
    main()
