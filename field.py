import pygame
from mutagen.mp3 import MP3 as mp3
from pygame.locals import *
import sys
import numpy as np
from board import board
from board import piece



class field():
    def __init__(self,pos):
        self.board = board(pos[0],pos[1])
        self.font = pygame.font.SysFont(None,80)

    def put(self,pos,c):
        if self.board.put(piece(pos[0],pos[1],c)):
            return -c
        else:
            return c

    def draw(self,screen):
        return self.board.draw(screen)

    #テスト用
    def test(self):
        return self.board.listBoard(1)
