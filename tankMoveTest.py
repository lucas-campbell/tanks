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
tankSprite = pygame.image.load('bluetank.png').convert()
tank_x, tank_y = tankSprite.get_size()
spriteSize = (40, 40)
smallTank = pygame.Surface(spriteSize)
pygame.transform.scale(tankSprite, spriteSize, smallTank)


def drawTank(x,y):
    """ Draws tank """
    gameDisplay.blit(smallTank, (x,y))


x =  (display_width * 0.5)
y = (display_height * 0.5)
cover_w, cover_h = smallTank.get_width() + 10, smallTank.get_height() + 10
old_rect = pygame.Rect((x,y), (cover_w, cover_h))
tank_speed = 0

gameDisplay.fill(white)
drawTank(x, y)
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
    old_rect = pygame.Rect((x,y), (cover_w, cover_h))
    x += x_change
    y += y_change
    rect_x = x - 10
    rect_y = y - 10
    to_update = pygame.Rect((rect_x, rect_y), (cover_w, cover_h))
    ##         
    white_pixels = pygame.Surface((old_rect.width, old_rect.height))
    white_pixels.fill(white)
    gameDisplay.blit(white_pixels, old_rect)

    drawTank(x,y)
        
    pygame.display.update([to_update, old_rect])
    clock.tick(60)

pygame.quit()
quit()
