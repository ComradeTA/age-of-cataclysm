import pygame
from util.button import Button
from gameworldDefaults.character import Character
from gameworldDefaults.game import Game
from gameworldDefaults.gameData import GameData
from gameworldDefaults.map import Map
import time
from PIL import Image
import numpy as np

class GameRenderer():
    def __init__(self, w, h, b_fullscreen = False):
        self.w = w
        self.h = h
        self.curr_x = 0
        self.curr_y = 0
        self.b_fullscreen = b_fullscreen
        self.map = Map("images/world_map_wallpaper.png", 1920*4, 1080*4)
        self.minimap_img = pygame.transform.scale(self.map.model, (int(w/10), int(h/10)))



    def render(self, game_display, game_data):
        game_display.blit(self.map.model, (0,0))

        game_display.blit(self.map.model.subsurface(pygame.Rect(self.curr_x, self.curr_y, self.w, self.h-200)), (0,40))

        #minimap
        game_display.blit(self.minimap_img, (5, self.h - self.h * 0.1 - 5))





