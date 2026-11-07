import math
import sys
import time

import pygame


WIDTH, HEIGHT = 1100, 700
FPS = 60
ROAD_WIDTH = 105
CAR_SIZE = (24, 42)
MAX_SPEED = 360
ACCELERATION = 250
BRAKE_POWER = 360
TURN_SPEED = 2.8
CRASH_SPEED = 55

BG = (35, 115, 55)
ROAD = (65, 67, 74)
ROAD_EDGE = (180, 180, 180)
WHITE = (245, 245, 245)
CAR_COLOR = (235, 55, 55)
YELLOW = (245, 210, 45)
BLACK = (18, 18, 20)


TRACKS = [
    {
        "name": "Oval Run",
        "points": [(180, 350), (260, 145), (520, 90), (820, 145), (920, 350), (820, 555), (520, 610), (260, 555)],
    },
    {
        "name": "Zigzag Circuit",
        "points": [(180, 520), (180, 180), (400, 100), (700, 180), (920, 100), (920, 520), (700, 600), (400, 520)],
    },
    {
        "name": "River Loop",
        "points": [(160, 220), (330, 100), (610, 120), (920, 250), (850, 500), (610, 600), (300, 540), (150, 390)],
    },
]


class Car:
    def __init__(self, start, heading):
        self.position = pygame.Vector2(start)
        self.heading = heading
        self.speed = 0.0
        self.crash_timer = 0.0

    def reset(self, start, heading):
        self.position = pygame.Vector2(start)
        self.heading = heading
        self.speed = 0.0
        self.crash_timer = 0.0

    def update(self, dt, track):
        keys = pygame.key.get_pressed()
        throttle = keys[pygame.K_w] or keys[pygame.K_UP]
        brake = keys[pygame.K_s] or keys[pygame.K_DOWN]

        if throttle:
            self.speed += ACCELERATION * dt
        elif brake:
            self.speed -= BRAKE_POWER * dt
        else:
            self.speed -= 80 * dt
        self.speed = max(0, min(MAX_SPEED, self.speed))

        if self.speed > 5:
            steering = keys[pygame.K_d] or keys[pygame.K_RIGHT]
            steering_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
            turn = bool(steering) - bool(steering_left)
            self.heading += turn * TURN_SPEED * dt * min(self.speed / 150, 1.6)

        direction = pygame.Vector2(math.cos(self.heading), math.sin(self.heading))
        self.position += direction * self.speed * dt

        distance = distance_to_loop(self.position, track["points"])
        if distance > ROAD_WIDTH / 2 - 8:
            self.speed *= 0.18
            self.crash_timer = 0.65
            self.position -= direction * min(45 * dt, self.speed * dt)

        self.crash_timer = max(0, self.crash_timer - dt)

    def draw(self, surface):
        body = pygame.Surface(CAR_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(body, CAR_COLOR, body.get_rect(), border_radius=5)
        pygame.draw.rect(body, (160, 210, 235), (4, 7, CAR_SIZE[0] - 8, 12), border_radius=3)
        rotated = pygame.transform.rotate(body, -math.degrees(self.heading) + 90)
        surface.blit(rotated, rotated.get_rect(center=self.position))


def distance_to_segment(point, start, end):
    segment = end - start
    if segment.length_squared() == 0:
        return point.distance_to(start)
    amount = max(0, min(1, (point - start).dot(segment) / segment.length_squared()))
    return point.distance_to(start + segment * amount)


def distance_to_loop(point, points):
    return min(
        distance_to_segment(point, pygame.Vector2(points[index]), pygame.Vector2(points[(index + 1) % len(points)]))
        for index in range(len(points))
    )


def nearest_waypoint(point, points):
    distances = [point.distance_to(pygame.Vector2(item)) for item in points]
    return min(range(len(points)), key=distances.__getitem__)


def passed_start_line(car, track, previous_waypoint, completed_waypoints):
    start = pygame.Vector2(track["points"][0])
    return completed_waypoints >= len(track["points"]) - 2 and car.position.distance_to(start) < 48


def draw_track(surface, track):
    points = [pygame.Vector2(point) for point in track["points"]]
    closed = points + [points[0]]
    pygame.draw.lines(surface, ROAD_EDGE, True, closed, ROAD_WIDTH + 12)
    pygame.draw.lines(surface, ROAD, True, closed, ROAD_WIDTH)

    for index in range(len(points)):
        start = points[index]
        end = points[(index + 1) % len(points)]
        pygame.draw.line(surface, (215, 215, 215), start, end, 2)

    start = points[0]
    direction = (points[1] - start).normalize()
    across = direction.rotate(90) * (ROAD_WIDTH / 2)
    for index in range(8):
        left = start - across + direction * (index * 14 - 52)
        right = start + across + direction * (index * 14 - 52)
        color = WHITE if index % 2 == 0 else BLACK
        pygame.draw.line(surface, color, left, right, 9)


def new_race(track):
    start = pygame.Vector2(track["points"][0])
    next_point = pygame.Vector2(track["points"][1])
    heading = math.atan2(next_point.y - start.y, next_point.x - start.x)
    return Car(start, heading), time.perf_counter(), 0, False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Three Track Time Trial")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    big_font = pygame.font.SysFont("arial", 48, bold=True)

    track_index = 0
    track = TRACKS[track_index]
    car, start_time, last_waypoint, finished = new_race(track)
    best_times = [None] * len(TRACKS)

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
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    track_index = event.key - pygame.K_1
                    track = TRACKS[track_index]
                    car, start_time, last_waypoint, finished = new_race(track)
                if event.key == pygame.K_r:
                    car, start_time, last_waypoint, finished = new_race(track)

        if not finished:
            car.update(dt, track)
            nearest = nearest_waypoint(car.position, track["points"])
            if (nearest - last_waypoint) % len(track["points"]) == 1:
                last_waypoint = nearest
            if passed_start_line(car, track, last_waypoint, last_waypoint):
                finished = True
                elapsed = time.perf_counter() - start_time
                if best_times[track_index] is None or elapsed < best_times[track_index]:
                    best_times[track_index] = elapsed

        elapsed = (time.perf_counter() - start_time) if not finished else elapsed
        screen.fill(BG)
        draw_track(screen, track)
        car.draw(screen)

        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 72))
        current_best = best_times[track_index]
        best_text = f"Best: {current_best:.2f}s" if current_best is not None else "Best: --"
        screen.blit(font.render(f"Track {track_index + 1}: {track['name']}", True, WHITE), (25, 16))
        screen.blit(font.render(f"Time: {elapsed:.2f}s   {best_text}", True, WHITE), (25, 43))
        screen.blit(font.render("WASD/arrows drive | 1-3 tracks | R restart | Esc quit", True, WHITE), (620, 25))

        if car.crash_timer > 0:
            warning = font.render("CRASH!", True, YELLOW)
            screen.blit(warning, warning.get_rect(center=(WIDTH // 2, 35)))

        if finished:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 135))
            screen.blit(overlay, (0, 0))
            title = big_font.render("FINISH!", True, WHITE)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
            message = font.render("Press R to race again or 1, 2, 3 to choose a track", True, WHITE)
            screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

        pygame.display.flip()


if __name__ == "__main__":
    main()
