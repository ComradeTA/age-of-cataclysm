import socket
from _thread import *
import pickle
from gameworldDefaults.game import Game
import time

class Server_Client:
    def __init__(self, addr, p, gameId = None):
        self.addr = addr
        self.p = p
        self.gameId = gameId
        self.conn_lost = 0

    def __str__(self):
        return "Player " + str(self.p)

    def change_GameId(self, gameId):
        self.gameId = gameId

    def update_Conn(self):
        self.conn_lost = time.time()


server = "127.0.0.1"
port = 28420
#AF_INET = IPv4         SOCK_STREAM = TCP              SOCK_DGRAM = UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

print("Waiting for a connection, Server Started")

connected = set()
players = {}
games = {}
idCount = 0
p = 0



def threaded_client(key):
    #s_client = players[key]
    #s.sendto(str.encode(str(p)), s_client.addr)
    players[key].update_Conn()
    while True:
        s_client = players[key]
        time.sleep(0.01)
        try:
            if s_client.gameId == None:
                print("Check threaded client")
                continue

            if time.time() - s_client.conn_lost >= 3:
                print("Timeout")
                break
            
            if s_client.gameId in games:
                if s_client.addr in connected:
                    return_data = []
                    game = games[s_client.gameId]
                    return_data.append(game)
                    s.sendto(pickle.dumps(return_data), s_client.addr)
                else:
                    break
                
        except Exception as e:
            print(e)
            print("thread")
            break
    
    try:
        s_client = players[key]
        connected.discard(s_client.addr)
        print("Player: " + str(s_client.p) + " lost connection")
    except Exception as e:
        print(e)
        print("Server Client error")

    try:
        game.remove_player(s_client.p)
        games_temp = []
        game_pop = None
        game_name = None

        for key in games:
                print(games[key])
                if len(games[key].gameData.characters) == 0:
                    game_name = games[key].name
                    game_pop = key
                    continue
                games_temp.append(games[key].name)
        games.pop(game_pop)
        print("Game: " + game_name + " has been removed")
        print("All active games: ", games_temp)
    except Exception as e:
            print(e)
            print("Game error")
    

while True:
    try:
        data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
        data = pickle.loads(data)
    except Exception as e:
        print(e)
        print("main")
        continue
    #print ("received message:", data, "from:", addr)
    
    if addr not in connected:
        p += 1
        print("Player ", str(p), " has connected from:", str(addr))
        start_new_thread(threaded_client, (p,))
        connected.add(addr)
        players[p] = Server_Client(addr, p)

    if data[1] == "host game":
        for key in games:
            if games[key].name == data[2]:
                return_data = [None, True]
                s.sendto(pickle.dumps(return_data), addr)
                connected.remove(addr)
                print("Player", data[0], "failed to host game:", data[2], "because it already exists")
                break
        else:
            games[idCount] = (Game(data[2], data[4], idCount, data[0], True))
            gameId = idCount
            idCount += 1
            game = games[gameId]
            game.add_player(data[0], data[3])
            players[data[0]].change_GameId(gameId)
            print("Player", data[0], "hosted game:", game.name)
            games_temp = []
            for key in games:
                games_temp.append(games[key].name)
            print("All active games: ", games_temp)
            return_data = [None, False]
            s.sendto(pickle.dumps(return_data), addr)
        continue

    elif data[1] == "join game":
        if len(games) == 0:
            return_data = [None, False]
            s.sendto(pickle.dumps(return_data), addr)
            connected.remove(addr)
            print("player", str(data[0]), "failed to join game:", data[2], "because there are no games")
            
            continue
        for key in games:
            if games[key].name == data[2]:
                game = games[key]
                players[data[0]].change_GameId(game.id)
                game.add_player(data[0], data[3])
                print("player", data[0], "is joining game:", str(game.name))
                return_data = [None, True]
                s.sendto(pickle.dumps(return_data), addr)
                break
            else:
                return_data = [None, False]
                s.sendto(pickle.dumps(return_data), addr)
                connected.remove(addr)
                print("player", str(data[0]), "failed to join game:", data[2], "because that game does not exist")
                break
        continue
                

    elif data[1] == "get":
         s.sendto(pickle.dumps(p), addr)
         continue

    elif data[1] == "disconnect":
        connected.remove(addr)

    elif data[1] == "update connection":
        players[data[0]].update_Conn()

    elif data[1] != "get":
        #print("Updating game")
        try:
            games[players[data[0]].gameId].play(data)
        except Exception as e:
            print(e)
        