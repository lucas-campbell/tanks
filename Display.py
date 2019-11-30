#!/usr/bin/env python3
import pygame

###########
# Functions called to command or query the display
###########
displayInit():
    """
    To be called from main client, possibly as separate process
    """
    pygame.init()
    

#TODO params
updateTankPosition(disp, tank_id, etc)
    # returns nothing
    pass

#TODO params
explodeTank(disp, tank_id, etc)
    # returns nothing
    pass

getReportedUserInput():
    # returns Message object to be sent over to Server, or simply to update
    # game state
    pass


gameOver(disp, won)
    """
    Displays message to user that they have lost or won
    """
    # returns nothing
    pass
