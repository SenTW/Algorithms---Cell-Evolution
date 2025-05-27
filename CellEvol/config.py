#here i will store some functions of separate cells 
# config.py - Configuration constants for the Cell Evolution Simulation

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Grid configuration
GRID_SIZE = 10
PANEL_HEIGHT = 100  # Height of the control panel at bottom

# Cell colors
RED = (255, 0, 0)       # Center cells
GREEN = (0, 255, 0)     # Shell cells
YELLOW = (255, 220, 0)  # UI highlight

# UI colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)  # Grid lines
BG_COLOR = (30, 30, 30)   # Background color

# Font settings
FONT_NAME = "Courier New"
FONT_SIZE = 20
FONT_BOLD = True

# Simulation settings
FPS = 60  # Frame rate
SIMULATION_SPEED = 1  # Simulation steps per frame

# Cell drawing settings
CELL_PADDING = 2  # Space between cells in the grid

# Derived grid dimensions (calculated automatically)
COLS = WIDTH // GRID_SIZE
ROWS = (HEIGHT - PANEL_HEIGHT) // GRID_SIZE

# Add these to your existing config.py
BASE_SPEED = 0.5  # Slower base speed
STAGE_SPEEDS = {
    1: 1.0,  # Fastest
    2: 0.6,
    3: 0.3   # Slowest
}