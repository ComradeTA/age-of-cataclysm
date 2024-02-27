import pygame

class Map():
    def __init__(self, img_path, w, h):
        self.w = w
        self.h = h
        self.model = pygame.transform.scale(pygame.image.load('images/world_map_wallpaper.png'), (w*4, h*4))
        self.grid = [[]]



