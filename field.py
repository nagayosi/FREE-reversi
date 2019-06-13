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
        self.bgm_end = pygame.mixer.Sound(os.path.join(music_path,"passionate.ogg"))
        self.bgm_end.set_volume(0.3)
        self.cant_put_se = pygame.mixer.Sound(os.path.join(music_path,"cant_put.ogg"))
        self.cant_put_se.set_volume(1.0)
        self.now_turn = 1

    def put(self,pos):
        if self.board.put(piece(pos[0],pos[1],self.now_turn)):
            self.now_turn = -self.now_turn
            if self.board.num == 40:
                pygame.mixer.stop()
                self.bgm_end.play(-1)
            return self.now_turn
        else:
            self.cant_put_se.play(1)
            return self.now_turn

    def pass_turn(self):
        self.now_turn = -self.now_turn


    def putdemo(self,pos,screen):
        pie = piece(pos[0],pos[1],self.now_turn)
        pie.draw(screen)


    def draw(self,screen):
        self.board.draw(screen)
        return self.isBattle()

    def isBattle(self):
        if self.board.num >= self.board.maxNum:
            return False
        else:
            return True

    def result(self):
        blackNum = len(self.board.listBoard(1))
        whiteNum = len(self.board.listBoard(-1))
        if blackNum > whiteNum:# black-win
            return 1
        elif blackNum < whiteNum:# white-win
            return -1
        else:# draw
            return 0
