import json
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
RECORD_FILE = "racing_records.json"

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
        "points": [(170, 350), (220, 180), (430, 90), (700, 90), (880, 180), (930, 350), (880, 520), (700, 610), (430, 610), (220, 520)],
    },
    {
        "name": "S-Curve",
        "points": [(150, 560), (220, 430), (390, 350), (560, 270), (730, 190), (930, 130), (930, 250), (760, 330), (590, 410), (420, 490), (250, 570)],
    },
    {
        "name": "Hairpin Hill",
        "points": [(170, 150), (430, 150), (760, 150), (930, 260), (930, 470), (760, 560), (430, 560), (210, 470), (210, 350), (430, 350), (700, 350), (760, 300), (700, 250), (430, 250), (170, 250)],
    },
]


def load_records():
    try:
        with open(RECORD_FILE, "r", encoding="utf-8") as file:
            records = json.load(file)
        return records if isinstance(records, list) and len(records) == 3 else [None, None, None]
    except (OSError, ValueError):
        return [None, None, None]


def save_records(records):
    try:
        with open(RECORD_FILE, "w", encoding="utf-8") as file:
            json.dump(records, file)
    except OSError:
        pass


class Car:
    def __init__(self, start, heading):
        self.position = pygame.Vector2(start)
        self.heading = heading
        self.velocity = pygame.Vector2()
        self.crash_timer = 0.0

    def update(self, dt, track):
        keys = pygame.key.get_pressed()
        forward = pygame.Vector2(math.cos(self.heading), math.sin(self.heading))
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity += forward * ACCELERATION * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity -= forward * BRAKE_POWER * dt

        forward_speed = self.velocity.dot(forward)
        steering = bool(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - bool(keys[pygame.K_a] or keys[pygame.K_LEFT])
        if abs(forward_speed) > 5 and steering:
            self.heading += steering * TURN_SPEED * dt * min(abs(forward_speed) / 150, 1.7)

        forward = pygame.Vector2(math.cos(self.heading), math.sin(self.heading))
        right = forward.rotate(90)
        longitudinal = forward * self.velocity.dot(forward)
        lateral = right * self.velocity.dot(right) * 0.94
        self.velocity = (longitudinal + lateral) * (0.996 if keys[pygame.K_w] or keys[pygame.K_UP] else 0.985)
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)

        self.position += self.velocity * dt
        if distance_to_loop(self.position, track["points"]) > ROAD_WIDTH / 2 - 8:
            self.velocity *= 0.18
            self.crash_timer = 0.65
            self.position -= self.velocity * dt * 2
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
    return min(distance_to_segment(point, pygame.Vector2(points[i]), pygame.Vector2(points[(i + 1) % len(points)])) for i in range(len(points)))


def nearest_waypoint(point, points):
    distances = [point.distance_to(pygame.Vector2(item)) for item in points]
    return min(range(len(points)), key=distances.__getitem__)


def crossed_start_line(previous, current, track):
    start = pygame.Vector2(track["points"][0])
    next_point = pygame.Vector2(track["points"][1])
    line_direction = (next_point - start).normalize()
    line_normal = line_direction.rotate(90)
    previous_side = (previous - start).dot(line_normal)
    current_side = (current - start).dot(line_normal)
    along = (current - start).dot(line_direction)
    return previous_side < 0 <= current_side and -ROAD_WIDTH / 2 <= along <= ROAD_WIDTH / 2


def draw_track(surface, track):
    points = [pygame.Vector2(point) for point in track["points"]]
    closed = points + [points[0]]
    # Circles at every join remove gaps at sharp S-curve and hairpin corners.
    pygame.draw.lines(surface, ROAD_EDGE, True, closed, ROAD_WIDTH + 12)
    pygame.draw.lines(surface, ROAD, True, closed, ROAD_WIDTH)
    for point in points:
        pygame.draw.circle(surface, ROAD_EDGE, point, (ROAD_WIDTH + 12) // 2)
        pygame.draw.circle(surface, ROAD, point, ROAD_WIDTH // 2)

    start = points[0]
    direction = (points[1] - start).normalize()
    across = direction.rotate(90) * (ROAD_WIDTH / 2)
    for index in range(8):
        left = start - across + direction * (index * 14 - 52)
        right = start + across + direction * (index * 14 - 52)
        pygame.draw.line(surface, WHITE if index % 2 == 0 else BLACK, left, right, 9)


def new_race(track):
    start = pygame.Vector2(track["points"][0])
    next_point = pygame.Vector2(track["points"][1])
    heading = math.atan2(next_point.y - start.y, next_point.x - start.x)
    return Car(start, heading), 0.0, start.copy(), 0, False


def centered_text(surface, font, message, y, color=WHITE):
    image = font.render(message, True, color)
    surface.blit(image, image.get_rect(center=(WIDTH // 2, y)))


def draw_menu(screen, title_font, font, selected, records):
    screen.fill(BG)
    centered_text(screen, title_font, "THREE TRACK TIME TRIAL", 100)
    centered_text(screen, font, "Choose a track, then press Enter", 155, (220, 230, 220))
    for index, track in enumerate(TRACKS):
        color = YELLOW if index == selected else WHITE
        record = f"Best: {records[index]:.2f}s" if records[index] is not None else "Best: --"
        centered_text(screen, font, f"{index + 1}. {track['name']}   {record}", 255 + index * 65, color)
    centered_text(screen, font, "Up/Down or 1-3 select | Enter start | Esc quit", 520)
    centered_text(screen, font, "WASD/arrows drive | Stay on the solid road", 555)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Three Track Time Trial")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    title_font = pygame.font.SysFont("arial", 48, bold=True)
    big_font = pygame.font.SysFont("arial", 72, bold=True)
    records = load_records()
    selected = 0
    mode = "menu"
    track = None
    car = None
    start_time = 0.0
    countdown = 0.0
    previous_position = pygame.Vector2()
    last_waypoint = 0
    completed_waypoints = 0
    elapsed = 0.0

    while True:
        dt = min(clock.tick(FPS) / 1000, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                if mode == "menu":
                    pygame.quit()
                    sys.exit()
                mode = "menu"
            elif mode == "menu":
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(TRACKS)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(TRACKS)
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    selected = event.key - pygame.K_1
                elif event.key == pygame.K_RETURN:
                    track = TRACKS[selected]
                    car, start_time, previous_position, last_waypoint, finished = new_race(track)
                    completed_waypoints = 0
                    countdown = 3.0
                    elapsed = 0.0
                    mode = "countdown"
            elif event.key == pygame.K_r and mode == "finished":
                car, start_time, previous_position, last_waypoint, finished = new_race(track)
                completed_waypoints = 0
                countdown = 3.0
                elapsed = 0.0
                mode = "countdown"

        if mode == "countdown":
            countdown -= dt
            if countdown <= 0:
                start_time = time.perf_counter()
                previous_position = car.position.copy()
                mode = "racing"
        elif mode == "racing":
            previous_position = car.position.copy()
            car.update(dt, track)
            nearest = nearest_waypoint(car.position, track["points"])
            if nearest == (last_waypoint + 1) % len(track["points"]):
                last_waypoint = nearest
                completed_waypoints += 1
            elapsed = time.perf_counter() - start_time
            if completed_waypoints >= len(track["points"]) and crossed_start_line(previous_position, car.position, track):
                mode = "finished"
                if records[selected] is None or elapsed < records[selected]:
                    records[selected] = elapsed
                    save_records(records)

        if mode == "menu":
            draw_menu(screen, title_font, font, selected, records)
        else:
            screen.fill(BG)
            draw_track(screen, track)
            car.draw(screen)
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 72))
            best = f"{records[selected]:.2f}s" if records[selected] is not None else "--"
            screen.blit(font.render(f"Track {selected + 1}: {track['name']}", True, WHITE), (25, 16))
            screen.blit(font.render(f"Time: {elapsed:.2f}s   Best: {best}", True, WHITE), (25, 43))
            screen.blit(font.render("WASD/arrows drive | R restart | Esc menu", True, WHITE), (760, 25))

            if mode == "countdown":
                centered_text(screen, big_font, str(max(1, math.ceil(countdown))), HEIGHT // 2, YELLOW)
            elif mode == "racing":
                centered_text(screen, font, "GO!", 35, YELLOW)
            elif mode == "finished":
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 135))
                screen.blit(overlay, (0, 0))
                centered_text(screen, big_font, "FINISH!", HEIGHT // 2 - 30)
                centered_text(screen, font, "Press R to race again or Esc for the menu", HEIGHT // 2 + 45)

        pygame.display.flip()


if __name__ == "__main__":
    main()
