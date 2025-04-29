import pygame

# Initialize PyGame
pygame.init()
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life (Editable Anytime)")
clock = pygame.time.Clock()

# Colors
BG_COLOR = (30, 30, 30)
ALIVE_COLOR = (0, 255, 0)
DEAD_COLOR = (50, 50, 50)

# Initialize grid
def create_grid():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

grid = create_grid()

# Count neighbors
def count_alive_neighbors(grid, x, y):
    count = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                count += grid[ny][nx]
    return count

# Update grid
def update_grid(grid):
    new_grid = create_grid()
    for y in range(ROWS):
        for x in range(COLS):
            alive = grid[y][x]
            neighbors = count_alive_neighbors(grid, x, y)
            if alive:
                new_grid[y][x] = 1 if neighbors in [2, 3] else 0
            else:
                new_grid[y][x] = 1 if neighbors == 3 else 0
    return new_grid

# Draw grid
def draw_grid(grid):
    for y in range(ROWS):
        for x in range(COLS):
            color = ALIVE_COLOR if grid[y][x] else DEAD_COLOR
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(screen, color, rect)

# Game loop
running = True
simulation_started = False

while running:
    screen.fill(BG_COLOR)
    draw_grid(grid)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse interaction (always allowed)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            col = mx // CELL_SIZE
            row = my // CELL_SIZE
            if 0 <= col < COLS and 0 <= row < ROWS:
                if event.button == 1:
                    grid[row][col] = 1  # Left-click: make cell alive
                elif event.button == 3:
                    grid[row][col] = 0  # Right-click: kill cell

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                simulation_started = True  # Start simulation

    if simulation_started:
        grid = update_grid(grid)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()

