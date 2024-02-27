import pygame
import math
from util.button import Button
from gameworldDefaults.character import Character
from gameworldDefaults.game import Game
from gameworldDefaults.gameData import GameData
from gameworldDefaults.tile import Tile
from util.network import Network
from util.characterDatabase import CharacterDatabase
from _thread import *
import noise
import time
from PIL import Image
import numpy as np

#________________________

pygame.init()

#_______________________

w = pygame.display.Info().current_w
h = pygame.display.Info().current_h
game_display = pygame.display.set_mode((w,h),pygame.FULLSCREEN)
w = 500
h = 500
game_display = pygame.display.set_mode((w,h), pygame.)
#_______________________

CharacterDatabase = CharacterDatabase()

world_size = 1000

inventory_ui = False

tile_texture = {}
tile = int(w/(1920/100))
tile_array = {}


tile_spritesheet = pygame.image.load('images/FOOD.png').convert()
#tile_water = tile_spritesheet.subsurface(pygame.Rect(0, 0, 50, 50))
tile_water = pygame.transform.scale(pygame.image.load('images/water_pixelart.png').convert(), (tile, tile))
tile_texture["water"] = tile_water

tile_ground = pygame.transform.scale(pygame.image.load('images/grass_pixelart.png').convert(), (tile, tile))
tile_texture["ground"] = tile_ground

tile_sand = pygame.transform.scale(pygame.image.load('images/sand_pixelart.png').convert(), (tile, tile))
tile_texture["sand"] = tile_sand



mainmenu_background_img = pygame.transform.scale(pygame.image.load('images/background.png').convert(), (w, h))

#_______________________

scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

#_______________________

font = pygame.font.SysFont("monospace", 20)
clock = pygame.time.Clock()
game = None

#______________________
#Buttons

play_button = Button("Play", (w-200)/2, (h/5)*1, (0,0,0))
settings_button = Button("Settings", (w-200)/2, (h/5)*2, (0,0,0))
exit_game_button = Button("Exit game", (w-200)/2, (h/5)*3, (0,0,0))
main_menu_button = Button("Main menu", (w-200)/2, (h/5)*3, (0,0,0))
singleplayer_button = Button("Singleplayer", (w-200)/2, (h/5)*1, (0,0,0))
multiplayer_button = Button("Multiplayer", (w-200)/2, (h/5)*2, (0,0,0))
seed_button = Button("", (w-200)/2, (h-200)/2, (0,0,0), True)
host_game_button = Button("Host game", (w-200)/2, (h/5)*1, (0,0,0))
join_game_button = Button("Join game", (w-200)/2, (h/5)*2, (0,0,0))
server_name_button = Button("", (w-200)/2, (h-200)/2, (0,0,0), True)
next_button = Button("Next", (w-200)/2 + 300, (h-200)/2, (0,0,0))
delete_character = Button("Delete", (w-200)/2 - 300, (h-200)/2, (0,0,0))
character_button = Button("", (w-200)/2, (h-200)/2, (0,0,0))
create_new_character_button = Button("Create new char", (w-200)/2, (h-500), (0,0,0))
create_character_button = Button("Create", (w-200)/2, (h-200)/2, (0,0,0))
character_name_button = Button("Create", (w-200)/2, (h-200)/3, (0,0,0), True)

#______________________



def update_game(n, p):
    global game
    connected = time.time()
    while True:
        game = n.receive()
        if time.time() - connected >= 1:
            n.send([p, "update connection"])
            connected = time.time()

def create_background_image():
    global mainmenu_background_img
    mainmenu_background = []
    for i in range(int(h/2-h), int(h/2)+1):
        temp_list = []
        for j in range(int(w/2-w), int(w/2)+1):
            current_tile = noise.pnoise2(i/scale, j/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            if current_tile <= -0.15:
                color = (0, 119, 190)
            elif current_tile <= -0.1:
                color = (194, 178, 128)
            else:
                color = (86, 176, 0)
            temp_list.append(color)
        mainmenu_background.append(temp_list)
    temp_img = Image.fromarray(np.array(mainmenu_background, dtype=np.uint8))
    temp_img.save('background.png')
    mode = temp_img.mode
    size = temp_img.size
    data = temp_img.tobytes()

    mainmenu_background_img = pygame.image.fromstring(data, size, mode)

def load_tiles():
    for i in range(-world_size, world_size):
        for j in range(-world_size, world_size):
            tile_id = str(i)+","+str(j)
            current_tile_number = noise.pnoise2(i/scale, j/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            if current_tile_number <= -0.15:
                current_tile_texture = "water"
                tile_array[tile_id] = Tile(current_tile_texture, False, False)
            elif current_tile_number <= -0.1:
                current_tile_texture = "sand"
                tile_array[tile_id] = Tile(current_tile_texture, True, True)
            else:
                current_tile_texture = "ground"
                tile_array[tile_id] = Tile(current_tile_texture, True, True)
                      

def draw_mainmenu(game_display, buttons):
    #pygame.draw.rect(game_display, (255,255,255), (0, 0, w, h))
    game_display.blit(mainmenu_background_img, (0,0))

    pygame.draw.rect(game_display, (0,0,0), (0, 0, 50, 50))
    fps = pygame.font.Font(None,30).render(
                                            str(int(clock.get_fps())), 
                                            True, 
                                            pygame.Color('white'))
    game_display.blit(fps, (10, 10))

    for b in buttons:
            b.draw(game_display)
    pygame.display.update()


def check_render(x, y, a, b):
    range_w = w/2
    range_h = h/2
    if abs(x-a) < range_w + 50:
        if abs(y-b) < range_h + 50:
            return True
        else:
            return False
    else:
        return False


def draw_game(game_display, game, p):
    global inventory_ui
    #pygame.draw.rect(game_display, (255,255,255), (0, 0, w, h))
    my_character = None

    for character in game.gameData.characters:
        if character.id == p:
            my_character = character

    for i in range(int((my_character.x - (w/2))/tile)-1,
                     int((my_character.x + (w/2))/tile)+1):
        for j in range(int((my_character.y - (h/2))/tile)-1,
                         int((my_character.y + (h/2))/tile)+1):
            tile_id = str(i)+","+str(j)
            current_tile = tile_array[tile_id]
            game_display.blit(tile_texture[current_tile.texture], (tile*i-my_character.x + int(w/2),
                                                                     tile*j-my_character.y + int(h/2)))


    for character in game.gameData.characters:
        if character.id == p:
            pygame.draw.circle(game_display,(255,255,0),(int(w/2), int(h/2)),(10))
        else:
            if check_render(my_character.x, my_character.y, character.x, character.y) is True:
                pygame.draw.circle(game_display,(255,0,255),(character.x-my_character.x + int(w/2),
                                                             character.y-my_character.y + int(h/2)),(10))

    
    info_str = "FPS: "+str(int(clock.get_fps()))+" Game: "+str(game.name)+" Player: "+str(my_character.id)+" x = "+str(my_character.x)+" y = "+str(my_character.y)
    info = pygame.font.Font(None,30).render(info_str, True, pygame.Color('white'))
    pygame.draw.rect(game_display, (0,0,0), (0, 0, 20 + 10 * len(info_str), 50))
    game_display.blit(info, (10, 10))
    
    pygame.display.update()


def physics(direction, game, p):
    for character in game.gameData.characters:
        if character.id == p:
            my_character = character

    dest_x = my_character.x
    dest_y = my_character.y
    if direction == "right":
        #x
        dest_x += my_character.velocity
    elif direction == "up":
        #-y
        dest_y -= my_character.velocity
    elif direction == "left":
        #-x
        dest_x -= my_character.velocity
    elif direction == "down":
        #y
        dest_y += my_character.velocity
    tile_x = int(dest_x/tile)
    tile_y = int(dest_y/tile)
    if dest_x < 0:
        tile_x -= 1
    if dest_y < 0:
        tile_y -= 1
    tile_id = str(tile_x)+","+str(tile_y)
    current_tile = tile_array[tile_id]
    #print(tile_id, current_tile.texture, current_tile.walkable)
    return current_tile.walkable

def run():
    global done, gamemode, multiplayer, gamemode_menu, game, inventory_ui
    #create_background_image()
    load_tiles()
    done = False
    gamemode = 1
    multiplayer = False
    gamemode_menu = 0
    host_game = True
    initialized = False
    character_name = ""
    character_index = 0
    
    while not done:
        clock.tick(60)
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        #main menu
        if gamemode == 0:
            if initialized == False:
                n = Network()
                p = int(n.get_P())
                print("You are character", p)
                print(character_name)
                if host_game == True:
                    n.send([p, "host game", server_name_button.text, character_name, "123456789"])
                    gamename_exist = n.receive()
                    print(gamename_exist)
                    if gamename_exist[1] == True:
                        gamemode = 1
                        host_game = False
                        continue
                else:
                    n.send([p, "join game", server_name_button.text, character_name])
                    game_exist = n.receive()
                    print(game_exist)
                    if game_exist[1] == False:
                        print("Game " + str(server_name_button.text) + " did not exist")
                        gamemode = 1
                        continue

                start_new_thread(update_game, (n, p))
                game = n.receive()
                initialized = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                if physics("right", game[0], p) is True:
                    n.send([p, "right"])
            if keys[pygame.K_w]:
                if physics("up", game[0], p) is True:
                    n.send([p, "up"])
            if keys[pygame.K_a]:
                if physics("left", game[0], p) is True:
                    n.send([p, "left"])
            if keys[pygame.K_s]:
                if physics("down", game[0], p) is True:
                    n.send([p, "down"])
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    n.send([p, "disconnect"])
                    done = True
                    
            draw_game(game_display, game[0], p)
            
        elif gamemode == 1:
            if gamemode_menu == 0:
                buttons = [play_button, settings_button, exit_game_button]
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for b in buttons:
                            if b.click(mouse_x, mouse_y) == True:
                                if b == buttons[0]:
                                    #play 
                                    gamemode_menu = 1
                                elif b == buttons[1]:
                                    #settings
                                    pass
                                elif b == buttons[2]:
                                    #Exit
                                    done = True

            elif gamemode_menu == 1:
                buttons = [singleplayer_button, multiplayer_button, main_menu_button]
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for b in buttons:
                            if b.click(mouse_x, mouse_y) == True:
                                if b == buttons[0]:
                                    #singleplayer
                                    multiplayer = False
                                    gamemode_menu = 2
                                elif b == buttons[1]:
                                    #Multiplayer
                                    multiplayer = True
                                    gamemode_menu = 3
                                elif b == buttons[2]:
                                    #Main menu
                                    gamemode_menu = 0

            elif gamemode_menu == 2:
                buttons = [seed_button, main_menu_button]

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for b in buttons:
                            if b.click(mouse_x, mouse_y) == True:
                                if b == buttons[0]:
                                    #seed
                                    b.text_input_active = True
                                elif b == buttons[1]:
                                    #Main menu
                                    gamemode_menu = 0
                            else:
                                b.text_input_active = False

                    #Key input
                    if event.type == pygame.KEYDOWN:
                        for b in buttons:
                            if b.text_input == True:
                                if b.text_input_active == True:
                                    if event.key == pygame.K_RETURN:
                                        pass
                                        #gamemode = 0
                                    elif event.key == pygame.K_BACKSPACE:
                                        b.text = b.text[:-1]
                                        
                                    else:
                                        b.text += event.unicode

            elif gamemode_menu == 3:
                buttons = [host_game_button, join_game_button, main_menu_button]
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for b in buttons:
                            if b.click(mouse_x, mouse_y) == True:
                                if b == buttons[0]:
                                    #Host game
                                    host_game = True
                                    gamemode_menu = 4
                                elif b == buttons[1]:
                                    #Join game
                                    host_game = False
                                    gamemode_menu = 4
                                elif b == buttons[2]:
                                    #Main menu
                                    gamemode_menu = 0

            elif gamemode_menu == 4:
                buttons = [server_name_button, main_menu_button]
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for b in buttons:
                            if b.click(mouse_x, mouse_y) == True:
                                if b == buttons[0]:
                                    #server name
                                    b.text_input_active = True
                                elif b == buttons[1]:
                                    #Main menu
                                    gamemode_menu = 0
                            else:
                                b.text_input_active = False

                    #Key input
                    if event.type == pygame.KEYDOWN:
                        for b in buttons:
                            if b.text_input == True:
                                if b.text_input_active == True:
                                    if event.key == pygame.K_RETURN:
                                        gamemode_menu = 5
                                    elif event.key == pygame.K_BACKSPACE:
                                        b.text = b.text[:-1]
                                    else:
                                        b.text += event.unicode
            #choose character
            elif gamemode_menu == 5:
                buttons = [next_button, character_button, create_new_character_button, delete_character]
                characters = CharacterDatabase.retrieve_Character_Names()
                if len(characters) > 0:
                    character_button.change_Text(characters[character_index])
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for b in buttons:
                            if b.click(mouse_x, mouse_y) == True:
                                if b == buttons[0]:
                                    #next
                                    character_index += 1
                                    if character_index > len(characters)-1:
                                        character_index = 0
                                    if len(characters) > 0:
                                        character_button.change_Text(characters[character_index])
                                    
                                elif b == buttons[1]:
                                    #character
                                    if buttons[1].text == "":
                                        pass
                                    else:
                                        character_name = characters[character_index]
                                        gamemode = 0
                                elif b == buttons[2]:
                                    gamemode_menu = 6
                                elif b == buttons[3]:
                                    CharacterDatabase.delete_Character(characters[character_index])
                                    character_index = 0

            #create character
            elif gamemode_menu == 6:
                buttons = [character_name_button, create_character_button]
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for b in buttons:
                            if b.click(mouse_x, mouse_y) == True:
                                if b == buttons[0]:
                                    #character name
                                    b.text_input_active = True
                                elif b == buttons[1]:
                                    #create and start
                                    if buttons[0].text == "":
                                        pass
                                    else:
                                        if CharacterDatabase.add_Character(character_name_button.text, 1) is True:
                                            character_name = character_name_button.text
                                            gamemode = 0
                                        else:
                                            pass
                            else:
                                b.text_input_active = False

                    #Key input
                    if event.type == pygame.KEYDOWN:
                        for b in buttons:
                            if b.text_input == True:
                                if b.text_input_active == True:
                                    if event.key == pygame.K_RETURN:
                                        pass
                                    elif event.key == pygame.K_BACKSPACE:
                                        b.text = b.text[:-1]
                                    else:
                                        b.text += event.unicode
                                

                            
                
            draw_mainmenu(game_display, buttons)

        
				
run()