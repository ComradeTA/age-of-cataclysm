import pygame
import math
from util.button import Button
from gameworldDefaults.character import Character
from gameworldDefaults.game import Game
from gameworldDefaults.gameData import GameData
from gameworldDefaults.tile import Tile
from gameRenderer import GameRenderer
from mainMenuRenderer import MainMenuRenderer
from util.network import Network
from util.localDatabase import LocalDatabase
from _thread import *
import noise
import time
from PIL import Image
import numpy as np

#________________________

class Client():
    def __init__(self):
        pygame.init()
        db = LocalDatabase()
        db.generate_Client_ID("temp")
        self.client_id = db.retrieve_clientID("temp")
        print(self.client_id)
        self.network = Network()
        self.game_data = GameData(123)
        self.b_run_client = True
        self.font = pygame.font.SysFont("monospace", 20)
        self.thread_identifier = None
        self.exit_flag = False
        self.exit_auto = time.time()
        self.start_time = time.time()

        w2 = pygame.display.Info().current_w
        h2 = pygame.display.Info().current_h

        self.w = w2/2
        self.h = h2/2

        self.b_fullscreen = False
        if (self.b_fullscreen):
            self.game_display = pygame.display.set_mode((self.w, self.h), pygame.FULLSCREEN)
        else:
            self.game_display = pygame.display.set_mode((self.w, self.h))

        self.mainMenuRenderer = MainMenuRenderer(self.w, self.h)
        self.gameRenderer = GameRenderer(self.w, self.h)

        self.run()
        

    def update_game(self):
        print("updating game thread running")
        connected = time.time()
        while (not self.exit_flag):
            self.game_data = self.network.receive()
            if time.time() - connected >= 1:
                self.network.send([self.client_id, "update connection"])
                connected = time.time()
        print("Thread dead")


    def connect(self):
        game_exist = self.network.connect(self.client_id, [self.client_id, "join game", "testServer", "testName"])
        print(game_exist)
        if game_exist[1] == False:
            print("Game did not exist")
            return
            
        self.thread_identifer = start_new_thread(self.update_game, ())


    def run(self):
        while self.b_run_client:
            self.exit_auto = time.time()

            print("render main menu")
            self.render_Main_Menu()

            if (self.b_run_client):
                print("render game")
                self.render_Game()
            

    def render_Game(self):
        render_game = True

        while render_game:
            self.exit_auto = time.time()
            self.gameRenderer.render(self.game_display, self.game_data)
            self.handle_game_input()

            pygame.display.update()



    def handle_game_input(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos

        print("handle keys")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.network.send([self.client_id, "right"])
            print("up")
        if keys[pygame.K_w]:
            self.network.send([self.client_id, "up"])
        if keys[pygame.K_a]:
            self.network.send([self.client_id, "left"])
        if keys[pygame.K_s]:
            self.network.send([self.client_id, "down"])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                print("quit")
                self.network.send([self.client_id, "disconnect"])



    def render_Main_Menu(self):
        render = True
        mouse_x = 0
        mouse_y = 0
        while render:
            self.exit_auto = time.time()
            self.mainMenuRenderer.render(self.game_display)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos

            
            if (self.mainMenuRenderer.check_Click(mouse_x, mouse_y)):
                self.connect()
                render = False

            pygame.display.update()

            #for event in pygame.event.get():
                #if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    #self.network.send([self.client_id, "disconnect"])
                    #render = False

        
                    
            
				
Client()