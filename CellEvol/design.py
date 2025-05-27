import pygame
from cells import CELL_STAGES

# Colors
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 220, 0)

# Font
pygame.font.init()
font = pygame.font.SysFont("Courier New", 20, bold=True)

GRID_SIZE = 10
PANEL_HEIGHT = 100

def draw_cell_from_layout(screen, x, y, stage):
    layout = CELL_STAGES.get(stage, [])
    for dx, dy, color in layout:
        cell_color = RED if color == "red" else GREEN
        pygame.draw.rect(screen, cell_color, (
            x + dx * GRID_SIZE,
            y + dy * GRID_SIZE,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        ))

def draw_grid(screen, width, height):
    for x in range(0, width, GRID_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, height - PANEL_HEIGHT))
    for y in range(0, height - PANEL_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (0, y), (width, y))

def draw_panel(screen, width, height):
    pygame.draw.rect(screen, WHITE, (0, height - PANEL_HEIGHT, width, PANEL_HEIGHT))
    draw_cell_from_layout(screen, 60, height - 70, 1)
    draw_cell_from_layout(screen, 160, height - 70, 2)
    draw_cell_from_layout(screen, 280, height - 70, 3)

    pygame.draw.rect(screen, YELLOW, (width - 120, height - 70, 100, 40))
    label = font.render("START", True, BLACK)
    screen.blit(label, (width - 95, height - 60))
