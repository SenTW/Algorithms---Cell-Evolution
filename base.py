import pygame
from color_palette import ColorPalette

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
DEAD_COLOR = (50, 50, 50)

# Initialize color palette
color_palette = ColorPalette(WIDTH, HEIGHT)
ALIVE_COLOR = color_palette.get_selected_color()

# Initialize grid
def create_grid():
    return [[(0, None) for _ in range(COLS)] for _ in range(ROWS)]  # (state, color)

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
                count += grid[ny][nx][0]  # Check only the state
    return count

# Update grid
def update_grid(grid):
    new_grid = create_grid()
    for y in range(ROWS):
        for x in range(COLS):
            alive, color = grid[y][x]
            neighbors = count_alive_neighbors(grid, x, y)
            if alive:
                new_grid[y][x] = (1 if neighbors in [2, 3] else 0, color)
            else:
                new_grid[y][x] = (1 if neighbors == 3 else 0, color)
    return new_grid

# Draw grid
def draw_grid(grid):
    for y in range(ROWS):
        for x in range(COLS):
            state, color = grid[y][x]
            cell_color = color if state and color else (ALIVE_COLOR if state else DEAD_COLOR)
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(screen, cell_color, rect)

# Game loop
running = True
simulation_started = False

while running:
    screen.fill(BG_COLOR)
    draw_grid(grid)
    color_palette.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse interaction (always allowed)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            
            # Check if click is in color palette
            if color_palette.handle_click((mx, my)):
                ALIVE_COLOR = color_palette.get_selected_color()
            else:
                # Handle grid clicks
                col = mx // CELL_SIZE
                row = my // CELL_SIZE
                if 0 <= col < COLS and 0 <= row < ROWS:
                    if event.button == 1:
                        grid[row][col] = (1, ALIVE_COLOR)  # Left-click: make cell alive with current color
                    elif event.button == 3:
                        grid[row][col] = (0, None)  # Right-click: kill cell

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                simulation_started = True  # Start simulation
            elif event.key == pygame.K_SPACE: # Space
                grid = create_grid()  # Reset grid
                simulation_started = False  # Stop simulation

    if simulation_started:
        grid = update_grid(grid)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()

