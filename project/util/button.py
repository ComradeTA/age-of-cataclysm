import pygame

class Button:
    def __init__(self, text, x, y, color, text_input = False,):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 200
        self.height = 100
        self.text_input = text_input
        if text_input is True:
            self.text = ""
            self.text_input_active = False

    def draw(self, game_display):
        pygame.draw.rect(game_display, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("monospace", 20)
        text = font.render(self.text, 1, (255,255,255))
        game_display.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, x, y):
        if self.x <= x and self.x + self.width >= x and self.y <= y and self.y + self.height >= y:
            return True
        else:
            return False

    def change_Text(self, new_text):
        self.text = new_text