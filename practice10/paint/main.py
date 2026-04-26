import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TOOLBAR_HEIGHT = 80

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)

MODE_BRUSH = "brush"
MODE_RECT = "rectangle"
MODE_CIRCLE = "circle"
MODE_ERASER = "eraser"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint Program")
clock = pygame.time.Clock()

class Button:
    def __init__(self, x, y, width, height, color, text="", text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 24)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class ColorPalette:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colors = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, 
                      CYAN, MAGENTA, ORANGE, PURPLE, GRAY]
        self.color_rects = []
        self.selected_color = BLACK
        
        for i, color in enumerate(self.colors):
            rect = pygame.Rect(x + i * 35, y, 30, 30)
            self.color_rects.append((rect, color))

    def draw(self, surface):
        for rect, color in self.color_rects:
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
            
            if color == self.selected_color:
                pygame.draw.rect(surface, WHITE, rect, 3)

    def check_click(self, pos):
        for rect, color in self.color_rects:
            if rect.collidepoint(pos):
                self.selected_color = color
                return True
        return False

def main():
    canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)
    
    drawing = False
    start_pos = None
    current_mode = MODE_BRUSH
    brush_size = 5
    current_color = BLACK
    eraser_size = 20
    
    buttons = [
        Button(10, 10, 80, 30, GRAY, "Brush"),
        Button(100, 10, 80, 30, GRAY, "Rect"),
        Button(190, 10, 80, 30, GRAY, "Circle"),
        Button(280, 10, 80, 30, GRAY, "Eraser"),
        Button(370, 10, 80, 30, WHITE, "Clear")
    ]
    
    color_palette = ColorPalette(10, 50)
    
    size_up_btn = Button(600, 10, 30, 30, GRAY, "+")
    size_down_btn = Button(640, 10, 30, 30, GRAY, "-")
    size_text_font = pygame.font.Font(None, 24)
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                if y < TOOLBAR_HEIGHT:
                    if buttons[0].is_clicked(event.pos):
                        current_mode = MODE_BRUSH
                    elif buttons[1].is_clicked(event.pos):
                        current_mode = MODE_RECT
                    elif buttons[2].is_clicked(event.pos):
                        current_mode = MODE_CIRCLE
                    elif buttons[3].is_clicked(event.pos):
                        current_mode = MODE_ERASER
                    elif buttons[4].is_clicked(event.pos):
                        canvas.fill(WHITE)
                    
                    if size_up_btn.is_clicked(event.pos):
                        brush_size = min(50, brush_size + 2)
                        eraser_size = min(50, eraser_size + 2)
                    elif size_down_btn.is_clicked(event.pos):
                        brush_size = max(1, brush_size - 2)
                        eraser_size = max(5, eraser_size - 2)
                    
                    color_palette.check_click(event.pos)
                    current_color = color_palette.selected_color
                
                else:
                    drawing = True
                    start_pos = (x, y - TOOLBAR_HEIGHT)
                    
                    if current_mode == MODE_BRUSH:
                        pygame.draw.circle(canvas, current_color, start_pos, brush_size)
                    elif current_mode == MODE_ERASER:
                        pygame.draw.circle(canvas, WHITE, start_pos, eraser_size)
            
            elif event.type == pygame.MOUSEMOTION:
                if drawing and current_mode in [MODE_BRUSH, MODE_ERASER]:
                    x, y = event.pos
                    if y > TOOLBAR_HEIGHT:
                        canvas_pos = (x, y - TOOLBAR_HEIGHT)
                        if current_mode == MODE_BRUSH:
                            pygame.draw.circle(canvas, current_color, canvas_pos, brush_size)
                        else:
                            pygame.draw.circle(canvas, WHITE, canvas_pos, eraser_size)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    x, y = event.pos
                    if y > TOOLBAR_HEIGHT:
                        end_pos = (x, y - TOOLBAR_HEIGHT)
                        
                        if current_mode == MODE_RECT:
                            rect = pygame.Rect(start_pos[0], start_pos[1], 
                                             end_pos[0] - start_pos[0], 
                                             end_pos[1] - start_pos[1])
                            pygame.draw.rect(canvas, current_color, rect, 2)
                        
                        elif current_mode == MODE_CIRCLE:
                            center = start_pos
                            radius = int(((end_pos[0] - center[0])**2 + 
                                        (end_pos[1] - center[1])**2)**0.5)
                            pygame.draw.circle(canvas, current_color, center, radius, 2)
                
                drawing = False
                start_pos = None
        
        screen.fill(GRAY)
        
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))
        
        pygame.draw.rect(screen, (200, 200, 200), (0, 0, SCREEN_WIDTH, TOOLBAR_HEIGHT))
        pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), 
                        (SCREEN_WIDTH, TOOLBAR_HEIGHT), 2)
        
        for button in buttons:
            button.draw(screen)
        
        color_palette.draw(screen)
        
        size_up_btn.draw(screen)
        size_down_btn.draw(screen)
        
        size_text = size_text_font.render(f"Size: {brush_size}", True, BLACK)
        screen.blit(size_text, (680, 15))
        
        mode_text = size_text_font.render(f"Mode: {current_mode.capitalize()}", 
                                          True, BLACK)
        screen.blit(mode_text, (500, 55))
        
        preview_x = 720
        preview_y = 50
        if current_mode == MODE_ERASER:
            pygame.draw.circle(screen, WHITE, (preview_x, preview_y), 10)
            pygame.draw.circle(screen, BLACK, (preview_x, preview_y), 10, 1)
        else:
            pygame.draw.circle(screen, current_color, (preview_x, preview_y), 10)
            pygame.draw.circle(screen, BLACK, (preview_x, preview_y), 10, 1)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()