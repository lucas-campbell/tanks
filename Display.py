#!/usr/bin/env python3
import pygame
import random
import errno
import Sprites # objects for sprite movement
from memory import *
from constants import *
from maps import *
from time import sleep

def show_reset_screen(screen, background, background_rect, clock, won=False, lost=False):
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
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    exit(0)
                elif event.key == pygame.K_SPACE:
                    waiting = False



font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def explode(exploding_player, sprites, screen, background, background_rect):
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
    
#### < TODO Add initial setup with server here > ####

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
    HEADERSIZE = 16
    HOST = input('SERVER IP:')
    PORT = 47477      
    player_num = 0
    player1_pos = Player_pos(pos = (20, 400), direct = UDLR.down)
    player2_pos = Player_pos(pos = (800-20, 400), direct = UDLR.up)
    players = [player1_pos, player2_pos]
    state = State(players, [[],[]], False) 

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.setblocking(0)
    is_connected = False
    other_player_ready = False


################## GAME LOOP ######################################
    running = True
    # Start out with reset screen
    game_over = True
    won = False
    lost = False
    while running:
        try:
            if not is_connected:
                print("Connected to server at IP:", HOST)
                data = client.recv(HEADERSIZE)
                player_num = int(data.decode())
                print("Player num:", player_num)
                is_connected = True
        except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                continue

        if game_over:
            show_reset_screen(screen, background, background_rect, clock, won, lost)
            game_over = False
            won = False
            lost = False

            # Create players and their sprites
            sprites = pygame.sprite.Group()
            
            client_is_p1 = (player_num == 1)

            player1 = Sprites.Player('high_res_blue_tank.png', 1, client_is_p1,
                                    player1_pos.position, player1_pos.direction)
            player2 = Sprites.Player('high_res_green_tank.png', 2, not client_is_p1,
                                    player2_pos.position, player2_pos.direction)
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

            #TODO change given info from server
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
            player_data = Memory(players[player_num-1], _ready = ready_for_new_game)
            data = pickle.dumps(player_data)
            msg_len = str(len(data))
            pack_header = '{:<{}}'.format(msg_len, HEADERSIZE)
            data = bytes(pack_header, 'utf-8')+data
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
                        #TODO determine which player we are
                        my_new_missiles.append(player.shoot(sprites, my_missiles))

            # Update: update sprite positions, send info to server and
            # receive info on other tank's position

            my_pos.position = (player.rect.centerx, player.rect.centery)
            my_pos.direction = player.direction

        ##### CLIENT COMM CODE #####
        #TODO possibly take out this second check
        if not is_connected:
            data = client.recv(HEADERSIZE)
            player_num = int(data.decode())
            print("Connected to server at IP:", HOST)
            print("Player Number:", player_num)
            is_connected = True
        else:
            #send information here
            try:
                #if not other_player_ready:
                #    my_new_missiles = []
                #    ready_for_new_game = True
                #else:
                #    ready_for_new_game = False
                if other_player_ready:
                    player_data = Memory(players[player_num-1], my_new_missiles, game_over, won, _ready = ready_for_new_game)
                    data = pickle.dumps(player_data)
                    msg_len = str(len(data))
                    pack_header = '{:<{}}'.format(msg_len, HEADERSIZE)
                    data = bytes(pack_header, 'utf-8')+data
                    client.sendall(data)

                #### wait for update here ###
                full_msg = b''
                new_msg = True
                end_msg = True

                while end_msg:
                    msg = client.recv(HEADERSIZE)

                    if not len(msg):
                        continue
                        #print('Connection closed by the server')
                        #exit()

                    if new_msg:
                        msg_header = msg[:HEADERSIZE]
                        msg_length = int(msg_header)
                        new_msg = False

                    full_msg += msg

                    #print(len(full_msg)), testing

                    if len(full_msg) - HEADERSIZE == msg_length:
                        #print("Got message")
                        data = pickle.loads(full_msg[HEADERSIZE:])
                        ### DATA MANIP/SCREEN UPDATES HERE ###
                        #Note: updating other player state
                        #print(data)
                        state = data
                        
                        end_msg = False
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                continue
            except Exception as e:
                print('Hit error: {}'.format(str(e)))
                sys.exit()

        game_state = state
        other_player_ready = game_state.ps_ready[other_player.player_number-1]
        # Go back and wait if other player not yet ready
        if not other_player_ready:
            continue
        new_enemy_missiles = game_state.missiles[other_player.player_number-1]
        if len(new_enemy_missiles) > 0:
            for m in new_enemy_missiles:
                new_enemy_missile = Sprites.Missile(m[0], m[1])
                their_missiles.add(new_enemy_missile)
                sprites.add(new_enemy_missile)

            
        sprites.update(game_state, obstacles)

        #TODO tank collision --> tie game

        p1_hit = pygame.sprite.spritecollide(player1, p2_missiles, dokill=True)
        p2_hit = pygame.sprite.spritecollide(player2, p1_missiles, dokill=True)

        if len(p1_hit) > 0:
            print("calculated explosion here")
            explode(player1, sprites, screen, background, background_rect)
            game_over = True
            ready_for_new_game = False
            if other_player.player_number == 1:
                won = True
            else:
                lost = True

           # player_data = Memory(players[player_num-1], my_new_missiles, game_over, won)
           # data = pickle.dumps(player_data)
           # msg_len = str(len(data))
           # pack_header = '{:<{}}'.format(msg_len, HEADERSIZE)
           # data = bytes(pack_header, 'utf-8')+data
           # client.sendall(data)


        elif len(p2_hit) > 0:
            print("calculated explosion here")
            explode(player2, sprites, screen, background, background_rect)
            game_over = True
            ready_for_new_game = False
            if other_player.player_number == 1:
                lost = True
            else:
                won = True

           # player_data = Memory(players[player_num-1], my_new_missiles, game_over, won)
           # data = pickle.dumps(player_data)
           # msg_len = str(len(data))
           # pack_header = '{:<{}}'.format(msg_len, HEADERSIZE)
           # data = bytes(pack_header, 'utf-8')+data
           # client.sendall(data)

        if game_over:
            sleep(2)

        # Draw / render
        #TODO remove fill black
        #screen.fill(BLACK)
        screen.blit(background, background_rect)
        #  Blits all sprites to screen
        sprites.draw(screen)
        # after drawing everything, flip the display

        # TODO possibly call display.update() with list of dirty rect's, for speed
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)

if __name__ == "__main__":
    GUI()
