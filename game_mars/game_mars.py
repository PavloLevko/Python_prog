import pygame
import random
import math

pygame.init()

# Розміри
WIDTH = 1000
HEIGHT = 600
MAP_WIDTH = 700
PANEL_WIDTH = 300

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mars Rover Mining")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 32)

# Кольори
MARS_RED = (170, 70, 50)
DARK_RED = (130, 40, 30)
CRATER = (110, 50, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (50, 200, 50)

# База
base_pos = (100, HEIGHT // 2)

# Каміння
rocks = []
for _ in range(15):
    rocks.append((
        random.randint(200, MAP_WIDTH - 50),
        random.randint(50, HEIGHT - 50)
    ))

# Кратери
craters = []
for _ in range(20):
    craters.append((
        random.randint(0, MAP_WIDTH),
        random.randint(0, HEIGHT),
        random.randint(10, 30)
    ))

# Ровер
class Rover:
    def __init__(self):
        self.x = base_pos[0]
        self.y = base_pos[1]
        self.target = random.choice(rocks)
        self.state = "to_rock"
        self.speed = 1.2

    def move(self):
        tx, ty = self.target
        dx = tx - self.x
        dy = ty - self.y

        dist = math.sqrt(dx*dx + dy*dy)

        if dist > 1:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed
        else:
            self.arrived()

    def arrived(self):
        global stone

        if self.state == "to_rock":
            self.target = base_pos
            self.state = "to_base"
        else:
            stone += 0.1
            self.target = random.choice(rocks)
            self.state = "to_rock"

    def update(self):
        self.move()

    def draw(self):
        pygame.draw.rect(screen, (220,220,220), (self.x, self.y, 10, 10))


rovers = [Rover()]

# Гра
stone = 0
level = 1
target_stone = 5

paused = False

rover_cost = 5
max_rovers = 5

# Кнопки
pause_btn = pygame.Rect(750, 50, 200, 40)
build_btn = pygame.Rect(750, 110, 200, 40)

def draw_button(rect, text, color=GRAY):
    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, BLACK)
    screen.blit(label, (rect.x + 10, rect.y + 10))


def draw_map():
    screen.fill(MARS_RED)

    # Кратери
    for x, y, r in craters:
        pygame.draw.circle(screen, CRATER, (x, y), r)

    # Каміння
    for x, y in rocks:
        pygame.draw.circle(screen, DARK_RED, (x, y), 6)

    # База
    pygame.draw.rect(screen, WHITE, (base_pos[0]-15, base_pos[1]-15, 30, 30))
    pygame.draw.polygon(screen, WHITE, [
        (base_pos[0], base_pos[1]-30),
        (base_pos[0]-10, base_pos[1]-15),
        (base_pos[0]+10, base_pos[1]-15)
    ])

    # Ровери
    for rover in rovers:
        rover.draw()


def draw_panel():
    pygame.draw.rect(screen, GRAY, (MAP_WIDTH, 0, PANEL_WIDTH, HEIGHT))

    stats = [
        f"Level: {level}",
        "",
        f"Stone: {round(stone,1)}",
        f"Target: {target_stone}",
        "",
        f"Rovers: {len(rovers)} / {max_rovers}",
        f"Cost: {round(rover_cost,1)}",
        "",
    ]

    y = 200
    for line in stats:
        text = font.render(line, True, BLACK)
        screen.blit(text, (750, y))
        y += 25


def next_level():
    global level, target_stone, stone
    level += 1
    stone = 0
    target_stone *= 1.8


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if pause_btn.collidepoint(mouse):
                paused = not paused

            if build_btn.collidepoint(mouse):

                if len(rovers) < max_rovers and stone >= rover_cost:
                    stone -= rover_cost
                    rovers.append(Rover())
                    rover_cost *= 1.5

    if not paused:
        for rover in rovers:
            rover.update()

    if stone >= target_stone:
        next_level()

    draw_map()
    draw_panel()

    draw_button(pause_btn, "Pause")
    draw_button(build_btn, "Build Rover", GREEN)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()