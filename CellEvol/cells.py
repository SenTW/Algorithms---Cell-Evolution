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
        self.to_be_removed = False
        self.direction = random.choice([
            (0, 1), (1, 0), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ])
        self.speed = BASE_SPEED * STAGE_SPEEDS[stage]

    def evolve_to_stage(self, new_stage):
        self.stage = new_stage
        if new_stage in STAGE_SPEEDS:
            self.speed = BASE_SPEED * STAGE_SPEEDS[new_stage]

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
        
        # 生態系ベースの相互作用
        collision_threshold = 1.5
        for other in all_cells:
            if other is not self:
                dx = other.grid_x - new_x
                dy = other.grid_y - new_y
                dist_squared = dx ** 2 + dy ** 2
                
                if dist_squared < collision_threshold:
                    
                    # 【改善された生態系モデル】
                    
                    # 1. 繁殖: 同じステージ同士が出会うと繁殖
                    if self.stage == other.stage and self.stage >= 2:
                        self.to_be_removed = True
                        other.to_be_removed = True
                        # 繁殖により新しい世代を生成
                        new_cells = []
                        for i in range(2):  # 2つの子供を生成
                            offset_x, offset_y = [(1, 0), (-1, 0)][i]
                            new_cell_x = max(min_x, min(self.grid_x + offset_x, max_x))
                            new_cell_y = max(min_y, min(self.grid_y + offset_y, max_y))
                            new_cells.append(Cell(new_cell_x, new_cell_y, 1))  # 新しい世代はステージ1から
                        return new_cells
                    
                    # 2. 成長: ステージ2がステージ1を「指導」してステージ3に成長
                    if self.stage == 2 and other.stage == 1:
                        self.evolve_to_stage(3)  # 指導経験で自分も成長
                        other.evolve_to_stage(2)  # 指導を受けて成長
                        return []
                    
                    # 3. 捕食: ステージ3がステージ1を「捕食」（自然な食物連鎖）
                    if self.stage == 3 and other.stage == 1:
                        other.to_be_removed = True  # ステージ1は捕食される
                        # ステージ3は栄養を得るが、過度の捕食で分裂圧が生まれる
                        # 一定確率で分裂（過栄養による細胞分裂をシミュレート）
                        if random.random() < 0.3:  # 30%の確率で分裂
                            self.to_be_removed = True
                            new_cells = []
                            for i in range(2):
                                offset_x, offset_y = [(1, 1), (-1, -1)][i]
                                new_cell_x = max(min_x, min(self.grid_x + offset_x, max_x))
                                new_cell_y = max(min_y, min(self.grid_y + offset_y, max_y))
                                new_cells.append(Cell(new_cell_x, new_cell_y, 2))  # 分裂後はステージ2
                            return new_cells
                        return []
                    
                    # 4. 競争: ステージ3 vs ステージ2（競争関係）
                    if (self.stage == 3 and other.stage == 2) or (self.stage == 2 and other.stage == 3):
                        # お互いにダメージを与える（競争）
                        if self.stage > other.stage:
                            other.evolve_to_stage(max(1, other.stage - 1))  # 相手を弱体化
                        else:
                            self.evolve_to_stage(max(1, self.stage - 1))  # 自分が弱体化
                        # 跳ね返り
                        if abs(dx) > abs(dy):
                            self.direction = (-self.direction[0], self.direction[1])
                        else:
                            self.direction = (self.direction[0], -self.direction[1])
                        return []
                    
                    # 5. 協力: ステージ1同士は群れを作る（跳ね返らない）
                    if self.stage == 1 and other.stage == 1:
                        # 群れ行動：同じ方向に移動
                        self.direction = other.direction
                        return []
                    
                    # 6. デフォルト: その他の場合は跳ね返り
                    if abs(dx) > abs(dy):
                        self.direction = (-self.direction[0], self.direction[1])
                    else:
                        self.direction = (self.direction[0], -self.direction[1])
                    return []
        
        # Update position if no collisions
        self.grid_x = new_x
        self.grid_y = new_y
        return []