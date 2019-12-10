###############
# Sprites.py
# Definition of Player, Missile, and Obstacle Sprites
###############
import pygame
from enum import Enum
from constants import *

class UDLR(Enum):
    up = 0
    down = 1
    left = 2
    right = 3

class Player(pygame.sprite.Sprite):
    def __init__(self, image_file_path, player_number, is_active_player, center, direction):
        self.player_number = player_number
        self.is_active_player = is_active_player
        pygame.sprite.Sprite.__init__(self)
        # Get image and corresponding rectangle
        self.image = pygame.image.load(image_file_path).convert()
        self.image = pygame.transform.scale(self.image, (TANK_H, TANK_W))
        self.original = self.image.copy()
        self.original.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = center[0]
        self.rect.centery = center[1]
        self.direction = direction
        # clear background for sprite
        self.image.set_colorkey(BLACK)

    def update(self, game_state, obstacles):
        """
        Implementation of pygame.sprite.Sprite.update method. Gets called for 
        each sprite in a Group with pygame.sprite.Group.update()
        Takes in a connection object used for communicating with the client
        middleman process. Calculates new position & waits for update on other
        tank's position, then updates display accordingly.
        """
        ### Process User Input ###

        # set in case no key was pressed
        new_direction = self.direction

        if self.is_active_player:
            keystate = pygame.key.get_pressed()
            # Side-side movement
            self.speedx = 0
            if keystate[pygame.K_LEFT]:
                self.speedx = -5
                new_direction = UDLR.left
            if keystate[pygame.K_RIGHT]:
                self.speedx = 5
                new_direction = UDLR.right

            # Out-of-bounds checking
            old_x = self.rect.x
            # Check for collision with obstacles
            self.rect.x += self.speedx
            crash = pygame.sprite.spritecollide(self, obstacles, dokill=False)
            if len(crash) > 0:
                self.rect.x = old_x
            elif self.rect.right > WIDTH:
                self.rect.right = WIDTH
            elif self.rect.left < 0:
                self.rect.left = 0

            # Up-down movement
            self.speedy = 0
            if keystate[pygame.K_DOWN]:
                self.speedy = 5
                new_direction = UDLR.down
            if keystate[pygame.K_UP]:
                self.speedy = -5
                new_direction = UDLR.up

            # Out-of-bounds checking
            old_y = self.rect.y
            # Check for collision with obstacles
            self.rect.y += self.speedy
            crash = pygame.sprite.spritecollide(self, obstacles, dokill=False)
            if len(crash) > 0:
                self.rect.y = old_y
            elif self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            elif self.rect.top < 0:
                self.rect.top = 0

        else:
            updated_pos = game_state.ps[self.player_number-1]
            self.rect.center = updated_pos.position
            new_direction = updated_pos.direction

        # Rotate sprite if necessary
        if new_direction != self.direction:
            self.rotate(new_direction)
        
        
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

    def shoot(self, sprites, missiles):
        if self.direction == UDLR.up:
            missile_center = (self.rect.centerx, self.rect.top - 4)
            missile = Missile(missile_center, UDLR.up)
        elif self.direction == UDLR.down:
            missile_center = (self.rect.centerx, self.rect.bottom + 4)
            missile = Missile(missile_center, UDLR.down)
        elif self.direction == UDLR.left:
            missile_center = (self.rect.left - 4, self.rect.centery)
            missile = Missile(missile_center, UDLR.left)
        else: # self.direction == UDLR.right
            missile_center = (self.rect.left + 4, self.rect.centery)
            missile = Missile(missile_center, UDLR.right)

        # Add to list of all sprites for updating, plus list of all missiles
        # for collisions
        sprites.add(missile)
        missiles.add(missile)
        ctr = (missile.rect.centerx, missile.rect.centery)
        return (ctr, missile.direction)

        

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, r):
        self.rect = r
        self.image = pygame.Surface((r.width, r.height))
        self.image.fill(dark_green)
        pygame.sprite.Sprite.__init__(self)
    def update(self, game_state, obstacles):
        pass


class Missile(pygame.sprite.Sprite):
    def __init__(self, center, direction):
        pygame.sprite.Sprite.__init__(self)
        # Get image
        self.image = pygame.image.load('spr_missile.png').convert()
        self.image = pygame.transform.scale(self.image, (MISSILE_W, MISSILE_H))

        # Set speed/direction for missile
        self.direction = direction
        if direction == UDLR.up:
            # image starts out as up, so no rotation needed
            self.speedx = 0
            self.speedy = -10
        elif direction == UDLR.down:
            self.image = pygame.transform.rotate(self.image, 180)
            self.speedx = 0
            self.speedy = 10
        elif direction == UDLR.left:
            self.image = pygame.transform.rotate(self.image, 90)
            self.speedx = -10
            self.speedy = 0
        else: # direction == UDLR.right:
            self.image = pygame.transform.rotate(self.image, -90)
            self.speedx = 10
            self.speedy = 0

        self.rect = self.image.get_rect()
        # Set starting position
        self.rect.center = center

        self.image.set_colorkey(WHITE)

    def update(self, game_state, obstacles):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # Check for collision with obstacles
        hit_obstacle = pygame.sprite.spritecollide(self, obstacles, dokill=False)
        if len(hit_obstacle) > 0:
            self.kill()

        elif self.rect.left < 0 or self.rect.right > WIDTH \
          or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
