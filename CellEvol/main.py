import pygame
import sys
import random
import time
from design import draw_grid, draw_panel, draw_cell_from_layout
from panel import Panel
from cells import Cell, CELL_STAGES
from config import *

# Initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cell Evolution Simulation - Infinite Loop")
clock = pygame.time.Clock()

# Game objects
panel = Panel(WIDTH, HEIGHT)
cells = []  # Stores Cell objects
simulation_running = False

# 無限ループシステムの設定
LAST_SPAWN_TIME = 0
SPAWN_INTERVAL = 3000  # 3秒ごとに新しいセルを生成
MIN_CELLS = 5  # 最小セル数
MAX_CELLS = 50  # 最大セル数
ENVIRONMENT_CHANGE_INTERVAL = 10000  # 10秒ごとに環境変化

def auto_spawn_cells(current_cells):
    """セル数が少なくなったら自動的に新しいセルを生成"""
    global LAST_SPAWN_TIME
    current_time = pygame.time.get_ticks()
    
    # セル数が最小値を下回った場合、または定期的にスポーン
    if (len(current_cells) < MIN_CELLS or 
        current_time - LAST_SPAWN_TIME > SPAWN_INTERVAL) and len(current_cells) < MAX_CELLS:
        
        # ランダムな位置にランダムなステージのセルを生成
        for _ in range(random.randint(1, 3)):
            x = random.randint(1, COLS - 2)
            y = random.randint(1, ROWS - 2)
            stage = random.choice([1, 1, 1, 2, 2, 3])  # ステージ1を多めに
            current_cells.append(Cell(x, y, stage))
        
        LAST_SPAWN_TIME = current_time
        print(f"Auto-spawned cells. Total: {len(current_cells)}")

def environmental_pressure(current_cells):
    """環境変化による圧力をシミュレート"""
    current_time = pygame.time.get_ticks()
    
    # 10秒ごとに環境変化
    if current_time % ENVIRONMENT_CHANGE_INTERVAL < 100:  # 短い時間窓で実行
        pressure_type = random.choice(["disease", "food_scarcity", "mutation"])
        
        if pressure_type == "disease" and len(current_cells) > 20:
            # 病気：ランダムにセルを除去
            victims = random.sample(current_cells, min(3, len(current_cells)))
            for cell in victims:
                cell.to_be_removed = True
            print("Environmental pressure: Disease outbreak!")
            
        elif pressure_type == "food_scarcity":
            # 食料不足：大きなセルにペナルティ
            for cell in current_cells:
                if cell.stage == 3 and random.random() < 0.3:
                    cell.evolve_to_stage(2)  # ステージダウン
            print("Environmental pressure: Food scarcity!")
            
        elif pressure_type == "mutation":
            # 突然変異：ランダムに進化
            lucky_cells = random.sample(current_cells, min(2, len(current_cells)))
            for cell in lucky_cells:
                if cell.stage < 3:
                    cell.evolve_to_stage(cell.stage + 1)
            print("Environmental pressure: Beneficial mutations!")

def get_ecosystem_stats(current_cells):
    """生態系の統計情報を取得"""
    stats = {1: 0, 2: 0, 3: 0}
    for cell in current_cells:
        stats[cell.stage] += 1
    return stats

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
            newly_created_cells = []  # このフレームで生まれる新しいセルを保存
            
            # 全てのセルを移動させる
            for cell in cells:
                new_cells_from_move = cell.move(COLS, ROWS, cells)
                if new_cells_from_move:
                    newly_created_cells.extend(new_cells_from_move)
            
            # 移動処理が完了してから、削除フラグが立ったセルを一括で除去
            cells = [cell for cell in cells if not cell.to_be_removed]
            
            # 新しく生成されたセルをリストに追加
            cells.extend(newly_created_cells)
            
            # 🔄 無限ループシステム
            # 1. 自動セル生成（セル数維持）
            auto_spawn_cells(cells)
            
            # 2. 環境圧力（バランス調整）
            environmental_pressure(cells)
            
            # 3. 統計情報の表示（5秒ごと）
            if pygame.time.get_ticks() % 5000 < 100:
                stats = get_ecosystem_stats(cells)
                print(f"Ecosystem: Stage1={stats[1]}, Stage2={stats[2]}, Stage3={stats[3]}, Total={len(cells)}")
        
        for cell in cells:
            pixel_x, pixel_y = cell.get_pixel_position()
            draw_cell_from_layout(screen, pixel_x, pixel_y, cell.stage)
        
        # Draw panel
        panel.draw(screen)
        
        # 🔄 リアルタイム統計表示
        if simulation_running:
            stats = get_ecosystem_stats(cells)
            font = pygame.font.Font(None, 24)
            
            # 統計情報をテキストで表示
            stats_text = f"Cells: S1={stats[1]} S2={stats[2]} S3={stats[3]} Total={len(cells)}"
            text_surface = font.render(stats_text, True, (255, 255, 255))
            screen.blit(text_surface, (10, HEIGHT - PANEL_HEIGHT - 30))
            
            # 時間表示
            time_text = f"Time: {pygame.time.get_ticks() // 1000}s"
            time_surface = font.render(time_text, True, (255, 255, 255))
            screen.blit(time_surface, (10, HEIGHT - PANEL_HEIGHT - 50))
        
        pygame.display.flip()
        clock.tick(FPS)  # Use FPS from config

if __name__ == "__main__":
    main()
