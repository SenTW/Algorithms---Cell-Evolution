import pygame
from cells import CELL_STAGES
from config import *

class Panel:
    def __init__(self, width, height):
        self.width = width
        self.height = PANEL_HEIGHT
        self.y_offset = height - PANEL_HEIGHT
        self.selected_stage = None
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE, FONT_BOLD)
        
        # Stage selection areas - wider boxes for better text fit
        self.stage_rects = {
            1: pygame.Rect(60, self.y_offset + 30, 100, 40),
            2: pygame.Rect(180, self.y_offset + 30, 100, 40),
            3: pygame.Rect(300, self.y_offset + 30, 100, 40)
        }
        
        # Start button
        self.start_rect = pygame.Rect(width - 120, self.y_offset + 30, 100, 40)

    def draw(self, screen):
        # Draw panel background
        pygame.draw.rect(screen, WHITE, (0, self.y_offset, self.width, self.height))
        
        # Draw stage selection boxes with centered text
        for stage, rect in self.stage_rects.items():
            color = YELLOW if self.selected_stage == stage else GREEN
            pygame.draw.rect(screen, color, rect)
            
            # Create and center the text
            text = self.font.render(f"Stage {stage}", True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # Draw start button with centered text
        pygame.draw.rect(screen, RED, self.start_rect)
        start_text = self.font.render("START", True, WHITE)
        start_text_rect = start_text.get_rect(center=self.start_rect.center)
        screen.blit(start_text, start_text_rect)

    def handle_click(self, pos):
        # Check stage selection
        for stage, rect in self.stage_rects.items():
            if rect.collidepoint(pos):
                self.selected_stage = stage
                return True
        
        # Check start button
        if self.start_rect.collidepoint(pos):
            return "start"
        
        return False

    def get_selected_stage(self):
        return self.selected_stage