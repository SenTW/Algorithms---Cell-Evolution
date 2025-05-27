import random
import pygame
from config import GRID_SIZE, COLS, ROWS, BASE_SPEED, STAGE_SPEEDS

CELL_STAGES = {
    1: [
        (0, 0, "red"),
        (-1, 0, "green"),
        (1, 0, "green"),
        (0, -1, "green"),
        (0, 1, "green")
    ],
    2: [
        (0, 0, "red"),
        (1, 0, "red"),
        (-1, 0, "green"),
        (2, 0, "green"),
        (0, -1, "green"),
        (1, -1, "green"),
        (0, 1, "green"),
        (1, 1, "green")
    ],
    3: [
        (0, 0, "red"),
        (1, 0, "red"),
        (0, 1, "red"),
        (1, 1, "red"),
        (-1, 0, "green"),
        (2, 0, "green"),
        (-1, 1, "green"),
        (2, 1, "green"),
        (0, -1, "green"),
        (1, -1, "green"),
        (0, 2, "green"),
        (1, 2, "green")
    ]
}


class Cell:
    def __init__(self, x, y, stage):
        self.grid_x = x
        self.grid_y = y
        self.stage = stage
        self.direction = random.choice([
            (0, 1), (1, 0), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ])
        self.speed = BASE_SPEED * STAGE_SPEEDS[stage]

    def get_pixel_position(self):
        return (
            int(self.grid_x * GRID_SIZE),
            int(self.grid_y * GRID_SIZE)
        )

    def get_occupied_positions(self):
        layout = CELL_STAGES[self.stage]
        return [
            (self.grid_x + dx, self.grid_y + dy)
            for dx, dy, _ in layout
        ]

    def move(self, grid_width, grid_height, all_cells):
    # Calculate new position
      new_x = self.grid_x + self.direction[0] * self.speed
      new_y = self.grid_y + self.direction[1] * self.speed
    
    # Bounce off walls
      min_x = 0
      min_y = 0
      max_x = grid_width - 1
      max_y = grid_height - 1
    
      if new_x < min_x or new_x > max_x:
          self.direction = (-self.direction[0], self.direction[1])
          new_x = max(min_x, min(new_x, max_x))  # Clamp position
      if new_y < min_y or new_y > max_y:
          self.direction = (self.direction[0], -self.direction[1])
          new_y = max(min_y, min(new_y, max_y))  # Clamp position
    
    # Bounce off other cells
      collision_threshold = 1.5  # Increased from 1.0 to make collisions less sensitive
      for other in all_cells:
        if other is not self:
            dx = other.grid_x - new_x
            dy = other.grid_y - new_y
            dist_squared = dx ** 2 + dy ** 2
            
            if dist_squared < collision_threshold:
                # Calculate reflection vector
                if abs(dx) > abs(dy):
                    self.direction = (-self.direction[0], self.direction[1])
                else:
                    self.direction = (self.direction[0], -self.direction[1])
                return  # Don't move this frame if collided
    
    # Update position if no collisions
        self.grid_x = new_x
        self.grid_y = new_y