import pygame
from enum import Enum

# Make sure these match the values in Display.py
WIDTH = 400
HEIGHT = 600

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class UDLR(Enum):
    up = 0
    down = 1
    left = 2
    right = 3

class Player(pygame.sprite.Sprite):
    def __init__(self, image_file_path, is_p1):
        self.is_p1 = is_p1
        pygame.sprite.Sprite.__init__(self)
        # Get image and corresponding rectangle
        self.image = pygame.image.load(image_file_path).convert()
        #TODO better scaling process(?), change to constants
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.original = self.image.copy()
        self.rect = self.image.get_rect()
        # sets starting position of sprite, TODO change with a ctor param
        if is_p1:
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        else:
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = 10
        # starting x/y speeds
        self.speedx = 0
        self.speedy = 0
        # starting direction
        self.direction = UDLR.up
        # clear background for sprite
        self.image.set_colorkey(WHITE)

    def update(self):
        #TODO possibly error checking done by server side instead of here.
        # But, may be faster to do here anyways.

        if self.is_p1:
            # Side-side movement
            self.speedx = 0
            keystate = pygame.key.get_pressed()
            # set in case no key was pressed
            new_direction = self.direction
            if keystate[pygame.K_LEFT]:
                self.speedx = -5
                new_direction = UDLR.left
            if keystate[pygame.K_RIGHT]:
                self.speedx = 5
                new_direction = UDLR.right

            self.rect.x += self.speedx
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

            # Up-down movement
            self.speedy = 0
            if keystate[pygame.K_DOWN]:
                self.speedy = 5
                new_direction = UDLR.down
            if keystate[pygame.K_UP]:
                self.speedy = -5
                new_direction = UDLR.up

            self.rect.y += self.speedy
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0

            if new_direction != self.direction:
                self.rotate(new_direction)
        else: # Then we are p2
            # Side-side movement
            self.speedx = 0
            keystate = pygame.key.get_pressed()
            # set in case no key was pressed
            new_direction = self.direction
            if keystate[pygame.K_a]:
                self.speedx = -5
                new_direction = UDLR.left
            if keystate[pygame.K_d]:
                self.speedx = 5
                new_direction = UDLR.right

            self.rect.x += self.speedx
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

            # Up-down movement
            self.speedy = 0
            if keystate[pygame.K_s]:
                self.speedy = 5
                new_direction = UDLR.down
            if keystate[pygame.K_w]:
                self.speedy = -5
                new_direction = UDLR.up

            self.rect.y += self.speedy
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0

            if new_direction != self.direction:
                self.rotate(new_direction)

        
        ##TODO: return above info as just x, y? Or whatever else Message obj needs
        # < Code for sending updated position to server > #
        ##

        
    def do_update(self):
        #TODO set updated variables to the new values, aka split update()
        # up into send_update() and do_update()
        pass

    def send_update(self):
        pass

    def rotate(self, new_direction):
        """ 
        Sets image to face the desired direction. NOTE: Assumes square sprites
        """
        # Note: rotations are counterclockwise by default in pygame
        if new_direction == UDLR.up:
            self.image = self.original
        elif new_direction == UDLR.down:
            self.image = pygame.transform.rotate(self.original, 180)
        elif new_direction == UDLR.left:
            self.image = pygame.transform.rotate(self.original, 90)
        else: #new_direction == UDLR.right
            self.image = pygame.transform.rotate(self.original, -90)
        self.direction = new_direction

    def shoot(self):
        if self.direction == UDLR.up:
            missile = Missile(args) #TODO

        

class Obstacle:()
    pass #TODO

class Missile(pygame.sprite.Sprite):
    def __init__((x, y), direction):
        pygame.sprite.Sprite.__init__(self)
        # Get image and corresponding rectangle
        self.image = pygame.image.load('spr_missile.png').convert()
        #TODO better scaling process(?), change to constants
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        # sets starting position of sprite, TODO set this automatically via
        # input from user on spacebar (shoot button?)
        #TODO if statements, set starting pos based on x/y
        self.rect.center = center
        # clear background for sprite
        self.image.set_colorkey(WHITE)

        # Set speed/direction for missile
        self.direction = direction
        if direction == UDLR.up:
            self.speedx = 0
            self.speedy = -10
        elif direction == UDLR.down:
            self.speedx = 0
            self.speedy = 10
        elif direction == UDLR.left:
            self.speedx = -10
            self.speedy = 0
        else: # direction == UDLR.left:
            self.speedx = 10
            self.speedy = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.left < 0 or self.rect.right > WIDTH \
          or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
