import pygame

class ColorPalette:
    def __init__(self, screen_width, screen_height):
        self.colors = [
            (0, 255, 0),    # green
            (255, 0, 0),    # red
            (0, 0, 255),    # blue
        ]
        self.selected_color = self.colors[0]
        self.palette_rect = pygame.Rect(screen_width - 100, 10, 80, 80)
        self.color_rects = []
        self.create_color_rects()

    def create_color_rects(self):
        color_height = 20
        for i, color in enumerate(self.colors):
            rect = pygame.Rect(
                self.palette_rect.x + 5,
                self.palette_rect.y + 5 + (i * (color_height + 5)),
                70,
                color_height
            )
            self.color_rects.append((rect, color))

    def draw(self, screen):
        # backround of the palette
        pygame.draw.rect(screen, (50, 50, 50), self.palette_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.palette_rect, 2)

        for rect, color in self.color_rects:
            pygame.draw.rect(screen, color, rect)
            if color == self.selected_color:
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)

    def handle_click(self, pos):
        for rect, color in self.color_rects:
            if rect.collidepoint(pos):
                self.selected_color = color
                return True
        return False

    def get_selected_color(self):
        return self.selected_color 