import pygame
from util.button import Button
from gameworldDefaults.character import Character
from gameworldDefaults.game import Game
from gameworldDefaults.gameData import GameData
from gameworldDefaults.map import Map
import time
from PIL import Image
import numpy as np
from util.button import Button


class MainMenuRenderer():
    def __init__(self, w, h):
        pygame.init()
        self.w = w
        self.h = h
        self.curr_x = 0
        self.curr_y = 0 
        self.background_img = pygame.transform.scale(pygame.image.load('images/world_map_wallpaper.png'), (w, h))
        self.game_display = None
        self.buttons = []
        self.buttons.append(Button("Play", (w-200)/2, (h/5), (0,0,0)))
        self.b_run_game = True
        self.clock = pygame.time.Clock()

    def render(self, game_display):
        game_display.blit(self.background_img, (0,0))

        for b in self.buttons:
            b.draw(game_display)

    def check_Click(self, x, y):
        for b in self.buttons:
            if b.click(x, y) == True:
                return True
            else:
                return False
        

