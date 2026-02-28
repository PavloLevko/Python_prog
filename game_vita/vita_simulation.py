import pygame
import random

pygame.init()

# ─── НАЛАШТУВАННЯ ────────────────────────────────────────
MAP_WIDTH = 700
MAP_HEIGHT = 700
PANEL_WIDTH = 300
TILE_SIZE = 10

WIDTH = MAP_WIDTH + PANEL_WIDTH
HEIGHT = MAP_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляція життя тварин")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)
font_small = pygame.font.SysFont("arial", 16)

# Кольори
BLUE      = (40,  120, 255)
GREEN     = (0,   180, 60)
ORANGE    = (255, 165, 0)
BROWN     = (140, 70,  20)
WHITE     = (255, 255, 255)
BLACK     = (0,   0,   0)
GRAY      = (230, 230, 240)
RED       = (220, 50,  50)
DARK_GRAY = (160, 160, 160)
YELLOW    = (240, 220, 100)
SICK_BROWN= (180, 60,  40)   # трохи червонуватий для хворих

cols = MAP_WIDTH // TILE_SIZE
rows = MAP_HEIGHT // TILE_SIZE

# ─── СВІТ ───────────────────────────────────────────────
world = []
for y in range(rows):
    row = []
    for x in range(cols):
        r = random.random()
        if r < 0.08:    row.append("water")
        elif r < 0.45:  row.append("grass")
        else:           row.append("land")
    world.append(row)

# ─── ТВАРИНИ ────────────────────────────────────────────
class Animal:
    def __init__(self):
        self.x = random.randint(0, cols - 1)
        self.y = random.randint(0, rows - 1)
        self.hunger = random.uniform(0, 6)
        self.thirst = random.uniform(0, 6)
        self.health = 100.0          # нове: здоров'я
        self.alive = True

    def update(self):
        if not self.alive:
            return

        self.hunger += 0.035
        self.thirst += 0.048

        # Рух — не кожен кадр
        if random.random() < 0.40:
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            self.x = max(0, min(cols - 1, self.x + dx))
            self.y = max(0, min(rows - 1, self.y + dy))

        tile = world[self.y][self.x]

        if tile == "grass":
            self.hunger = max(0, self.hunger - 14)
            world[self.y][self.x] = "land"
        elif tile == "water":
            self.thirst = max(0, self.thirst - 18)
            world[self.y][self.x] = "land"

        # Зменшення здоров'я при критичних станах
        if self.hunger > 18:
            self.health -= 0.4 + (self.hunger - 18) * 0.15
        if self.thirst > 20:
            self.health -= 0.5 + (self.thirst - 20) * 0.20

        # Смерть
        if self.health <= 0:
            self.alive = False
            self.health = 0

    def get_state(self):
        if not self.alive:
            return "Померла"
        if self.thirst > 14:
            return "Шукає воду"
        if self.hunger > 12:
            return "Шукає їжу"
        if self.health < 40:
            return "Хвора / Вмирає"
        return "Блукає"

    def get_draw_color(self):
        if not self.alive:
            return (90, 90, 90)           # сірий — труп
        if self.health < 35:
            return SICK_BROWN             # червоно-коричневий — хвора
        return BROWN

    def draw(self, surface):
        if not self.alive and random.random() < 0.03:
            return  # іноді не малюємо труп (імітація розкладання)

        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, self.get_draw_color(), rect)
        if self.alive:
            pygame.draw.rect(surface, YELLOW, rect, width=1)

# Створюємо тварин
animals = [Animal() for _ in range(12)]   # можна змінити кількість

# ─── СТАН СИМУЛЯЦІЇ ─────────────────────────────────────
simulation_running = True
drought_mode = False

# Кнопки (без змін)
buttons = {
    "toggle_sim": pygame.Rect(720,  40, 220, 45),
    "add_grass":  pygame.Rect(720, 110, 220, 45),
    "add_water":  pygame.Rect(720, 170, 220, 45),
    "drought":    pygame.Rect(720, 230, 220, 45),
}

def draw_button(rect, text, bg_color, text_color=BLACK):
    pygame.draw.rect(screen, bg_color, rect, border_radius=6)
    pygame.draw.rect(screen, DARK_GRAY, rect, width=2, border_radius=6)
    label = font.render(text, True, text_color)
    tw, th = label.get_size()
    screen.blit(label, (rect.centerx - tw//2, rect.centery - th//2))

def count_resources():
    water = grass = land = 0
    for row in world:
        for tile in row:
            if tile == "water": water += 1
            elif tile == "grass": grass += 1
            else: land += 1
    return water, grass, land

def add_grass_tiles():
    for _ in range(60):
        x, y = random.randint(0, cols-1), random.randint(0, rows-1)
        world[y][x] = "grass"

def add_water_tiles():
    for _ in range(50):
        x, y = random.randint(0, cols-1), random.randint(0, rows-1)
        if world[y][x] == "land":
            world[y][x] = "water"

def apply_drought_effect():
    for y in range(rows):
        for x in range(cols):
            if world[y][x] == "water" and random.random() < 0.014:
                world[y][x] = "land"
            if world[y][x] == "grass" and random.random() < 0.009:
                world[y][x] = "land"

# ─── ГОЛОВНИЙ ЦИКЛ ──────────────────────────────────────
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if buttons["toggle_sim"].collidepoint(pos):
                simulation_running = not simulation_running
            if buttons["add_grass"].collidepoint(pos):
                add_grass_tiles()
            if buttons["add_water"].collidepoint(pos):
                add_water_tiles()
            if buttons["drought"].collidepoint(pos):
                drought_mode = not drought_mode

    screen.fill((18, 18, 28))

    # Карта
    for y in range(rows):
        for x in range(cols):
            tile = world[y][x]
            color = ORANGE
            if tile == "water": color = BLUE
            elif tile == "grass": color = GREEN
            pygame.draw.rect(screen, color,
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Оновлення та малювання тварин
    if simulation_running:
        for animal in animals:
            animal.update()
        if drought_mode:
            apply_drought_effect()

    for animal in animals:
        animal.draw(screen)

    # Панель
    pygame.draw.rect(screen, GRAY, (MAP_WIDTH, 0, PANEL_WIDTH, HEIGHT))

    # Кнопки
    draw_button(buttons["toggle_sim"], "Старт / Пауза", (80,200,80) if simulation_running else (140,140,160))
    draw_button(buttons["add_grass"],  "Додати траву", GREEN)
    draw_button(buttons["add_water"],  "Додати воду", BLUE)
    draw_button(buttons["drought"],    "Посуха", RED if drought_mode else (100,100,120))

    # Статистика
    water_cnt, grass_cnt, land_cnt = count_resources()

    alive_count = sum(1 for a in animals if a.alive)
    dead_count = len(animals) - alive_count

    states_count = {"Шукає воду": 0, "Шукає їжу": 0, "Блукає": 0, "Хвора / Вмирає": 0, "Померла": 0}
    for a in animals:
        st = a.get_state()
        states_count[st] = states_count.get(st, 0) + 1

    stats = [
        "Симуляція",
        "──────────────",
        f"Тварин усього:   {len(animals)}",
        f"Живих:           {alive_count}",
        f"Померлих:        {dead_count}",
        "",
        f"Вода:          {water_cnt:4d}   Трава: {grass_cnt:4d}",
        "",
        "Стани живих тварин:",
        f"  Шукає воду:   {states_count['Шукає воду']}",
        f"  Шукає їжу:    {states_count['Шукає їжу']}",
        f"  Блукає:       {states_count['Блукає']}",
        f"  Хвора:        {states_count['Хвора / Вмирає']}",
        "",
        f"Посуха: {'увімк' if drought_mode else 'вимк'}"
    ]

    y = 300
    for line in stats:
        color = BLACK if "────────" not in line else (90,90,110)
        text = font_small.render(line, True, color)
        screen.blit(text, (725, y))
        y += 26

    pygame.display.flip()
    clock.tick(12)

pygame.quit()