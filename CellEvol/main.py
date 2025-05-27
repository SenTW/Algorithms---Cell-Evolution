import pygame
import sys
from design import draw_grid, draw_panel, draw_cell_from_layout
from panel import Panel
from cells import Cell, CELL_STAGES
from config import *

# Initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cell Evolution Simulation")
clock = pygame.time.Clock()

# Game objects
panel = Panel(WIDTH, HEIGHT)
cells = []  # Stores Cell objects
simulation_running = False

def main():
    global simulation_running, cells
    
    while True:
        # Handle events first
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    result = panel.handle_click(event.pos)
                    if result == "start":
                        simulation_running = not simulation_running
                        print(f"Simulation {'running' if simulation_running else 'paused'}")
                    
                    # Place new cell if clicked on grid
                    elif event.pos[1] < HEIGHT - PANEL_HEIGHT and panel.get_selected_stage():
                        grid_x = event.pos[0] // GRID_SIZE
                        grid_y = event.pos[1] // GRID_SIZE
                        cells.append(Cell(grid_x, grid_y, panel.get_selected_stage()))

        # Clear screen
        screen.fill(BG_COLOR)
        
        # Draw grid
        draw_grid(screen, WIDTH, HEIGHT)
        
        # Update and draw all cells
        if simulation_running:
            # 全てのセルを移動させる
            for cell in cells:
                cell.move(COLS, ROWS, cells)
            
            # 移動処理が完了してから、削除フラグが立ったセルを一括で除去
            cells = [cell for cell in cells if not cell.to_be_removed]
        
        for cell in cells:
            pixel_x, pixel_y = cell.get_pixel_position()
            draw_cell_from_layout(screen, pixel_x, pixel_y, cell.stage)
        
        # Draw panel
        panel.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)  # Use FPS from config

if __name__ == "__main__":
    main()
