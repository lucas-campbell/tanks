#!/usr/bin/env python3
import pygame
import random
import Sprites # objects for sprite movement


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


def gameOver(disp, won):
    """
    Displays message to user that they have lost or won
    """
    # returns nothing
    pass

# TODO delete
def drawTank(disp,x,y):
    """ Draws tank """
    disp.blit(smallTank, (x,y))

############################# MAIN DRIVER ########################



def main():
    WIDTH = 400
    HEIGHT = 600
    FPS = 60

    # define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # initialize pygame and create window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Concurrent Tanks")
    clock = pygame.time.Clock()

    # Create players and their sprites
    sprites = pygame.sprite.Group()
    #TODO call constructor with correct images, plus indicator of P1/P2
    player1 = Sprites.Player('high_res_blue_tank.png', True)
    player2 = Sprites.Player('high_res_green_tank.png', False)
    sprites.add(player1) 
    sprites.add(player2) 

    # Game loop
    running = True
    while running:
        # keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT:
                    player1.shoot()
                elif event.key == pygame.K_LSHIFT:
                    player2.shoot()

        # Update: update sprite positions, send info to server/ get back
        # confirmations. TODO add server communication
        sprites.update()

        # Draw / render
        screen.fill(BLACK)
        # TODO possibly blit instead
        sprites.draw(screen)
        # after drawing everything, flip the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
