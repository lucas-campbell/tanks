#!/usr/bin/env python3
import pygame
import random
import Sprites # objects for sprite movement
import memory

WIDTH = 800
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

###########
# Functions called to command or query the display
###########
def displayInit():
    """
    To be called from main client, possibly as separate process
    """
    pygame.init()

    ####
    # Code for setting game display/width goes here,
    #  + call to pygame.display.set_mode(), set caption, etc.
    # set clock, colors, crashed bool, load sprites
    ####
    

#TODO params
def updateTankPosition(disp, tank_id, etc):
    drawTank(disp, x, y)
    # returns nothing
    pass

#TODO params
def explodeTank(disp, tank_id, etc):
    # returns nothing
    pass

def getReportedUserInput():
    # returns Message object to be sent over to Server, or simply to update
    # game state
    pass


def show_reset_screen(screen, background, background_rect, clock, won, lost):
    """
    Displays message to user that they have lost or won
    """
    pygame.init()
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

def explode(player, screen, background, background_rect, hits):
    screen.blit(background, background_rect)
    explosion = pygame.image.load('explosion.png').convert()
    explosion = pygame.transform.scale(explosion, player.rect.size)
    explosion_rect = explosion.get_rect()
    explosion_rect.center = player.rect.center
    screen.blit(explosion, explosion_rect)
    pygame.display.flip()
    while True:
        pass

############################# MAIN DRIVER #########################



def GUI(conn, active_is_p1):
    
##################  SETUP   #######################################
    # initialize pygame and create window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Concurrent Tanks")
    background = pygame.image.load('background.png').convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()
    clock = pygame.time.Clock()

################## GAME LOOP ######################################
    running = True
    # Start out with reset screen
    game_over = True
    while running:

        if game_over:
            show_reset_screen(screen, background, background_rect, clock, False, False)
            game_over = False

            # Create players and their sprites
            sprites = pygame.sprite.Group()
            player1 = Sprites.Player('high_res_blue_tank.png', is_p1=True, active_is_p1)
            player2 = Sprites.Player('high_res_green_tank.png', is_p1=False, !active_is_p1)
            sprites.add(player1) 
            sprites.add(player2) 
            # Create group of missiles to keep track of hits
            # TODO do same for obstacles
            p1_missiles = pygame.sprite.Group()
            p2_missiles = pygame.sprite.Group()


        # keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE
                #TODO determine which player we are
                player.shoot()

        #####  < CODE FOR COMMS WITH SERVER GOES HERE > #####

        # Update: update sprite positions, send info to server/ get back
        # confirmations. TODO add server communication
        game_state = State() #TODO get from Server
        sprites.update(game_state)

        #hits = pygame.hits.collisions()
        #if hits()
        ##TODO fill in
        #conn.send(Memory())

        p1_hit = pygame.sprite.spritecollide(player1, p2_missiles, False)
        p2_hit = pygame.sprite.spritecollide(player2, p1_missiles, False)

        if len(p1_hit) > 0:
            explode(player1, screen, background, background_rect, p1_hit)
        elif len(p2_hit) > 0:
            explode(player2, screen, background, background_rect, p2_hit)

        # Draw / render
        #TODO remove fill black
        #screen.fill(BLACK)
        screen.blit(background, background_rect)
        #  Blits all sprites to screen
        sprites.draw(screen)
        # after drawing everything, flip the display
        # TODO possibly call display.update() with list of dirty rect's
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)

if __name__ == "__main__":
    main()
