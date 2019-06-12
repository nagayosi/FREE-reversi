import pygame
from mutagen.mp3 import MP3 as mp3
from pygame.locals import *
import sys
import numpy as np
from board import board
from board import piece
import os


class field():
    def __init__(self,pos):
        self.board = board(pos[0],pos[1])
        self.font = pygame.font.SysFont(None,80)
        music_path = os.path.join(os.getcwd(),"music")
        pygame.mixer.init()
        self.bgm = pygame.mixer.Sound(os.path.join(music_path,"bacchus.ogg"))
        self.bgm.set_volume(0.3)
        self.bgm.play(-1)
        self.cant_put_se = pygame.mixer.Sound(os.path.join(music_path,"cant_put.ogg"))
        self.cant_put_se.set_volume(1.0)

    def put(self,pos,c):
        if self.board.put(piece(pos[0],pos[1],c)):
            return -c
        else:
            self.cant_put_se.play(1)
            return c

    def putdemo(self,pos,c,screen):
        pie = piece(pos[0],pos[1],c)
        pie.draw(screen)


    def draw(self,screen):
        return self.board.draw(screen)

    # def result(self):
    #     if self.board.num >= self.board.maxNum:
    #
