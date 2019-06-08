import pygame
from pygame.locals import *
import pygame.sprite as sprite
import numpy as np
import sys

class MySprite(sprite.Sprite):
    def __init__(self,x,y,filename):
        sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x+width/2
        self.y = y+height/2
        self.rect = Rect(x,y,width,height)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

    def changeImage(self,filename):
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(x,y,width,height)

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class lineSprite(sprite.Sprite):
    def __init__(self,x,y,surf):
        sprite.Sprite.__init__(self)
        surf.fill((255,0,0))
        self.image = surf
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(x,y,width,height)
        pygame.draw.line(self.image,(255,0,0),self.rect.topleft,self.rect.bottomright,2)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

    def draw(self,screen):
        screen.blit(self.image,self.rect)
