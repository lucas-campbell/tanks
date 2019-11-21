import pygame

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
#background = pygame.Surface(gameDisplay)
pygame.display.set_caption('A bit Racey')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False
tankSprite = pygame.image.load('tank.png').convert()
tank_x, tank_y = tankSprite.get_size()
smallTank = pygame.Surface((10,10))
pygame.transform.scale(tankSprite, (10, 10), smallTank)


def drawTank(x,y):
    """ Draws tank """
    gameDisplay.blit(smallTank, (x,y))


x =  (display_width * 0.5)
y = (display_height * 0.5)
old_rect = pygame.Rect((x,y), (20, 20))
car_speed = 0

gameDisplay.fill(white)
pygame.display.update()

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        ############################
        x_change, y_change = 0, 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
            elif event.key == pygame.K_RIGHT:
                x_change = 5
            elif event.key == pygame.K_UP:
                y_change = -5
            elif event.key == pygame.K_DOWN:
                y_change = 5
                
        ######################
    ##
    old_rect = pygame.Rect((x,y), (20, 20))
    x += x_change
    y += y_change
    rect_x = x - 10
    rect_y = y - 10
    to_update = pygame.Rect((rect_x, rect_y), (20, 20))
    ##         
    white_pixels = pygame.Surface((old_rect.width, old_rect.height))
    white_pixels.fill(white)
    gameDisplay.blit(white_pixels, old_rect)

    drawTank(x,y)
        
    pygame.display.update([to_update, old_rect])
    clock.tick(30)

pygame.quit()
quit()
