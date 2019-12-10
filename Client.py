#!/usr/bin/env python3
import pygame
import random
import errno
import socket
import Sprites # objects for sprite movement
from Messaging import *
from constants import *
from maps import *
from time import sleep
import copy

def add_header(data):
    '''Adds a header to a Bytes object'''
    msg_len = str(len(data))
    pack_header = '{:<{}}'.format(msg_len, HEADERSIZE)
    return bytes(pack_header, 'utf-8')+data

def show_reset_screen(screen, background, background_rect, clock, connection,\
                      won=False, lost=False):
    """
    Displays message to user that they have lost or won
    """
    #pygame.init()
    screen.blit(background, background_rect)
    if won:
        draw_text(screen, "You Win!!", 32, WIDTH/2, HEIGHT/4)
    elif lost:
        draw_text(screen, "You Lose :(", 32, WIDTH/2, HEIGHT/4)
    else: # we are starting game for the first time
        draw_text(screen,
                  "Use the arrow keys to move, and SPACE to shoot",
                  32, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Press SPACE to begin, or ESC to quit", \
                        32, WIDTH/2, HEIGHT/2)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()

                # SEND QUIT MSG TO SERVER #
                ending = pickle.dumps(-1)
                ending = add_header(ending)
                connection.sendall()
                
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()

                    # SEND QUIT MSG TO SERVER #
                    ending = pickle.dumps(-1)
                    ending = add_header(ending)
                    connection.sendall(ending)
                    
                    exit(0)
                elif event.key == pygame.K_SPACE:
                    waiting = False



font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    """
    Draws text on a given surface, but does not flip() the pygame display
    """
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def explode(exploding_player, sprites, screen, background, background_rect):
    """
    Draw explosion on screen and flip() to show to user
    """
    # Create explosion in correct place
    explosion = pygame.image.load('explosion.png').convert()
    explosion = pygame.transform.scale(explosion, exploding_player.rect.size)
    explosion.set_colorkey(WHITE)
    explosion_rect = explosion.get_rect()
    explosion_rect.center = exploding_player.rect.center

    # Draw resulting screen
    screen.blit(background, background_rect)
    sprites.draw(screen)
    screen.blit(explosion, explosion_rect)
    pygame.display.flip()
    

############################# MAIN DRIVER #########################



def GUI():
    """
    Main driver for client functionality. Connects with server, then loops
    getting information from user and sending/receving updates from the server
    """
    
##################  SETUP   #######################################
    # initialize pygame and create window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Concurrent Tanks")
    background = pygame.image.load('background.png').convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()
    clock = pygame.time.Clock()


############## CLIENT STATE SETUP #################################
    HOST = input('SERVER IP:')
    PORT = 47477      
    player_num = 0
    player1_start = Player_pos(pos = P1_START, direct = UDLR.up)
    player2_start = Player_pos(pos = P2_START, direct = UDLR.up)
    player1_pos = copy.deepcopy(player1_start)
    player2_pos = copy.deepcopy(player2_start)
    players = [player1_pos, player2_pos]
    state = State(players, [[],[]], False) 

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.setblocking(0)
    is_connected = False
    other_player_ready = False


################## GAME LOOP ######################################
    running = True
    # Start out with reset screen #
    game_over = True
    won = False
    lost = False
    
    while running:
        # GET PLAYER NUMBER #
        try:
            if not is_connected:
                print("Connected to server at IP:", HOST)
                data = client.recv(HEADERSIZE)
                player_num = int(data.decode())
                is_connected = True
        # COULD NOT GET PLAYER NUMBER #
        except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                continue

        if game_over:
            show_reset_screen(screen, background, background_rect, clock,\
                              client, won, lost)
            game_over = False
            won = False
            lost = False

            # Create players and their sprites
            sprites = pygame.sprite.Group()
            
            # Need to keep track of which sprite to update when we receive
            # keyboard updates
            client_is_p1 = (player_num == 1)

            player1 = Sprites.Player('high_res_blue_tank.png', 1, client_is_p1,
                                    player1_start.position,
                                    player1_pos.direction)
            player2 = Sprites.Player('high_res_green_tank.png', 2,
                                    not client_is_p1, player2_start.position,
                                    player2_pos.direction)
            sprites.add(player1) 
            sprites.add(player2) 
            # Create group of missiles to keep track of hits
            p1_missiles = pygame.sprite.Group()
            p2_missiles = pygame.sprite.Group()
            # Do same for obstacles
            obstacles = pygame.sprite.Group()
            obstacle_list = []
            for obst in map1:
                new_obst = Sprites.Obstacle(obst)
                obstacle_list.append(new_obst)
            for obst in obstacle_list:
                obstacles.add(obst)
                sprites.add(obst)

            # Aliases, may just name them appropriately above
            if player_num == 1:
                print("I am player 1")
                player = player1
                other_player = player2
                my_pos = player1_pos
                my_missiles = p1_missiles
                their_missiles = p2_missiles
            else:
                print("I am player 2")
                player = player2
                other_player = player1
                my_pos = player2_pos
                my_missiles = p2_missiles
                their_missiles = p1_missiles

            ready_for_new_game = True
            player_data = Memory(players[player_num-1],
                                 _ready = ready_for_new_game)
            data = pickle.dumps(player_data)
            data = add_header(data)
            client.sendall(data)

            ######### End Setup Loop #########

        if other_player_ready:
            # keep loop running at the right speed
            clock.tick(FPS)
            # Process input (events)
            my_new_missiles = []
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        my_new_missiles.append(player.shoot(sprites,
                                                            my_missiles))

            # Update: update sprite positions, send info to server and
            # receive info on other tank's position

            my_pos.position = (player.rect.centerx, player.rect.centery)
            my_pos.direction = player.direction

        ##### CLIENT COMM CODE #####
        try:
            # SEND FOR NEW GAME #
            if other_player_ready:
                player_data = Memory(players[player_num-1], my_new_missiles,
                                     game_over, won,
                                     _ready = ready_for_new_game)
                data = pickle.dumps(player_data)
                data = add_header(data)
                client.sendall(data)

            # WAIT FOR UPDATE #
            full_msg = b''
            new_msg = True
            end_msg = True

            # GET A FULL MESSAGE FROM SERVER #
            while end_msg:
                msg = client.recv(HEADERSIZE)

                # MSG EMPTY, DO NOTHING #
                if not len(msg):
                    continue

                # STARTING A NEW MESSAGE #
                if new_msg:
                    msg_header = msg[:HEADERSIZE]
                    msg_length = int(msg_header)
                    new_msg = False

                full_msg += msg

                # GOT FULL MESSAGE #
                if len(full_msg) - HEADERSIZE == msg_length:
                    data = pickle.loads(full_msg[HEADERSIZE:])
                    # DATA UPDATES HERE #
                    if data == -1:
                        print("Connection closed by server, quitting..")
                        exit(1)
                    else:    
                        state = data
                    
                    end_msg = False
        # CHECK FOR 0 BYTE MESSAGES (NON-BLOCKING SOCKETS) #
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            continue
        # HANDLE OTHER ERRORS #
        except Exception as e:
            print('Hit error: {}'.format(str(e)))
            sys.exit()

        game_state = state
        other_player_ready = game_state.ps_ready[other_player.player_number-1]
        # WAIT ON OTHER PLAYER #
        if not other_player_ready:
            continue
        new_enemy_missiles = game_state.missiles[other_player.player_number-1]
        if len(new_enemy_missiles) > 0:
            for m in new_enemy_missiles:
                new_enemy_missile = Sprites.Missile(m[0], m[1])
                their_missiles.add(new_enemy_missile)
                sprites.add(new_enemy_missile)

            
        # Calls each sprite's update() method within the group
        sprites.update(game_state, obstacles)

        # Check for collisions with enemy missiles
        p1_hit = pygame.sprite.spritecollide(player1, p2_missiles, dokill=False)
        p2_hit = pygame.sprite.spritecollide(player2, p1_missiles, dokill=False)

        if len(p1_hit) > 0:
            explode(player1, sprites, screen, background, background_rect)
            game_over = True
            ready_for_new_game = False
            if other_player.player_number == 1:
                won = True
            else:
                lost = True

            # Game is over, so send se4rver info that we are not ready for a
            # new game yet
            player_data = Memory(players[player_num-1], my_new_missiles,
                                 game_over, won, _ready=False)
            data = pickle.dumps(player_data)
            data = add_header(data)
            client.sendall(data)


        elif len(p2_hit) > 0:
            explode(player2, sprites, screen, background, background_rect)
            game_over = True
            ready_for_new_game = False
            if other_player.player_number == 1:
                lost = True
            else:
                won = True

            # Game is over, so send se4rver info that we are not ready for a
            # new game yet
            player_data = Memory(players[player_num-1], my_new_missiles,
                                 game_over, won, _ready=False)
            data = pickle.dumps(player_data)
            data = add_header(data)
            client.sendall(data)

        if game_over:
            # Slight Delay for explosions to persist on screen
            sleep(2)

        # Draw / render
        screen.blit(background, background_rect)
        # Blits all sprites to screen
        sprites.draw(screen)
        # after drawing everything, flip the display

        # Update what the user sees
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)

if __name__ == "__main__":
    GUI()
