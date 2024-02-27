import socket
from _thread import *
import pickle
from gameworldDefaults.game import Game
import time


class Server_Client:
    def __init__(self, addr, client_id, game_name = "testServer"):
        self.addr = addr
        self.client_id = client_id
        self.game_name = game_name
        self.conn_lost = 0

    def __str__(self):
        return "Player " + str(self.p)

    def change_game_name(self, game_name):
        self.game_name = game_name

    def update_Conn(self):
        self.conn_lost = time.time()


class Server():
    def __init__(self):
        self.server = "127.0.0.1"
        self.port = 28420
        #AF_INET = IPv4         SOCK_STREAM = TCP              SOCK_DGRAM = UDP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.games = {}
        self.games["testServer"] = Game("testServer", 123, 123)
        self.b_run_server = True

        self.connected_addrs = set()
        self.players = {}
        self.desired_delay = 1 / 64


        try:
            self.socket.bind((self.server, self.port))
        except socket.error as e:
            str(e)
        
        print("Waiting for a connection, Server Started")

        self.run()


    
    def threaded_client(self, key):
        #s_client = players[key]
        #s.sendto(str.encode(str(p)), s_client.addr)
        self.players[key].update_Conn()
        server_client = self.players[key]
        while True:
            time.sleep(0.01)
            # Send data to the client
            try:
                if server_client.game_name == None:
                    print("Client " + server_client.client_id + " did not properly get assigned a game(ID)")
                    break

                if time.time() - server_client.conn_lost >= 60:
                    print("Client " + server_client.client_id +" timed out")
                    break

                if server_client.game_name in self.games:
                    if server_client.addr in self.connected_addrs:
                        return_data = []
                        game = self.games[server_client.game_name]
                        return_data.append(game.get_gameData())
                        self.socket.sendto(pickle.dumps(return_data), server_client.addr)
                    else:
                        print("Client " + server_client.client_id + " game id is connected to a game or their addr is not in connected")
                        break   
            except Exception as e:
                print(e)
                print("Server thread failed to send data to its client")
                break

        # handle removal of client from server once connection is broken
        try:
            self.connected_addrs.discard(server_client.addr)
            print("Player: " + str(server_client.client_id) + " lost connection")
        except Exception as e:
            print(e)
            print("Server thread failed to discard a clients address after lost connection")

        # handle removal of client from game data
        try:
            game = self.games[server_client.game_name]
            game.get_gameData().remove_client_id(server_client.client_id)
        except Exception as e:
                print(e)
                print("Server thread failed to remove client from game data")


    def join_game(self, client_id, game_name, addr):
        #make sure a game exists
        if len(self.games) == 0:
            return_data = [None, False]
            self.socket.sendto(pickle.dumps(return_data), addr)
            self.connected_addrs.remove(addr)
            print("player", str(client_id), "failed to join game:", game_name, "because there are no games")
            return False

        #Add to addresses connected
        if (addr not in self.connected_addrs):
            print("Player ", client_id, " has connected from:", str(addr))
            start_new_thread(self.threaded_client, (client_id,))
            self.connected_addrs.add(addr)
            self.players[client_id] = Server_Client(addr, client_id)

        # Find the game an connect the player to that game
        for key in self.games:
            if self.games[key].name == game_name:
                game = self.games[key]
                self.players[client_id].change_game_name(game.name)
                game.get_gameData().add_client_id(client_id)
                print("player", client_id, "is joining game:", str(game.name))
                return_data = [None, True]
                print("sending return data")
                self.socket.sendto(pickle.dumps(return_data), addr)
            else:
                return_data = [None, False]
                self.socket.sendto(pickle.dumps(return_data), addr)
                self.connected_addrs.remove(addr)
                print("player", str(client_id), "failed to join game:", game_name, "because that game does not exist")
                print ("games " + str(self.games))
                return False

    def tick_manager(self, ticks, start_time, track_tick_time):
        # Check if one second has elapsed
        if time.time() - start_time >= 1:
            # Print the number of ticks per second
            print("Ticks per second:", ticks)
            
            # Reset tick counter and start time for the next interval
            ticks = 0
            start_time = time.time()

        end_time = time.time()  # Record the end time of each iteration

        # Calculate the time taken for the iteration
        print(end_time)
        print(track_tick_time)
        iteration_time = end_time - track_tick_time
        print(iteration_time)
        # If the iteration took less time than desired_delay, sleep for the remaining time
        if iteration_time < self.desired_delay:
            print("eep")
            time.sleep(self.desired_delay - iteration_time)

    def run(self):

        #ticks = 0  # Initialize tick counter
        #start_time = time.time()  # Record the start time of the interval

        #handle incoming packages from clients
        while self.b_run_server:
            #track_tick_time = time.time()
            #ticks += 1  # Increment tick counter
            # Load latest data
            try:
                data, addr = self.socket.recvfrom(1024) # buffer size is 1024 bytes
                data = pickle.loads(data)
            except Exception as e:
                print(e)
                continue
            #print ("received message:", data, "from:", addr)

            # Upon first connection, add address in the connected set, and start a threaded client
            if data[1] == "join game":
                self.join_game(data[0], data[2], addr)
                continue

            elif data[1] == "disconnect":
                self.connected_addrs.remove(addr)

            elif data[1] == "update connection":
                self.players[data[0]].update_Conn()

            #self.tick_manager(ticks, start_time, track_tick_time)
            

Server()