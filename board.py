import pygame
from mutagen.mp3 import MP3 as mp3
from pygame.locals import *
import sys
import numpy as np
from mySprite import MySprite,lineSprite
import os
import pdb

figpath = "figure"

class piece():
    def __init__(self,x,y,c):
        if c > 0:
            filename = os.path.join(figpath,"black.png")
        elif c < 0:
            filename = os.path.join(figpath,"white.png")
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        #中心座標（sprite.x,sprite.y）
        self.sprite = MySprite(x-width/2,y-height/2,filename)
        self.color = c

    def turn(self,c):
        self.c = c
        if self.c > 0:
            filename = os.path.join(figpath,"black.png")
        elif self.c < 0:
            filename = os.path.join(figpath,"white.png")
        self.sprite.changeImage(filename)

    def calcDist(self,piece):#piece間距離
        x = piece.sprite.x
        y = piece.sprite.y
        dist = ((self.sprite.x - x)**2 + (self.sprite.y - y)**2)**0.5

        return dist

    def draw(self,screen):
        self.sprite.draw(screen)




class board():
    def __init__(self,x,y):
        filename = os.path.join(figpath,"board.png")
        self.sprite = MySprite(x,y,filename)
        self.bd = []
        self.num = 0
        self.maxNum = 48
        #距離の閾値
        self.r_thre = 100
        #色と色との線
        self.lines = None


    #置いたらTrue置けなかったらFalse
    def put(self,piece):
        if self.putable(piece):
            self.lines = self.calcLine(piece)
            self.turn(piece,self.lines)
            self.bd.append(piece)
            self.num += 1
            return True
        return False

    #置いたときに重なるかどうかチェック
    def putable(self,piece):
        if self.num >= self.maxNum:
            return False

        for i,p in enumerate(self.bd):
            if pygame.sprite.collide_mask(piece.sprite,p.sprite):
                return False
        return True

    # 引数cと同じ色をリストにする
    def listBoard(self,c):
        result = []
        for i in range(len(self.bd)):
            if self.bd[i].color == c:
                result.append(self.bd[i])

        return result

    #spriteとして線を保存
    def calcLine(self,pie):
        c = pie.color
        sprite = pie.sprite

        #置く色と同じ色をリストに
        same_color_list = self.listBoard(c)
        lineList = []

        for p in same_color_list:
            offx = sprite.x - p.sprite.x
            offy = sprite.y - p.sprite.y

            if offx < 0:
                x = sprite.x
                offx = abs(offx)
            else:
                x = p.sprite.x

            if offy < 0:
                y = sprite.y
                offy = abs(offy)
            else:
                y = p.sprite.y

            surf = pygame.Surface((offx,offy),pygame.SRCALPHA)
            # pygame.draw.line(surf,(255,0,0),(sprite.x,sprite.y),(p.sprite.x,p.sprite.y),2)
            lineList.append(lineSprite(x,y,surf))

        return lineList


    def turn(self,piece,lines):
        c = piece.color

        for line in lines:
            collide = []
            col_ind = []
            for j,pie in enumerate(self.bd):
                if pygame.sprite.collide_mask(line,pie.sprite):
                        collide.append(pie)
                        col_ind.append(j)

            dists = np.array([collide[i].calcDist(piece) for i in range(len(collide))])

            #距離順にSort
            index = np.argsort(dists)
            dists = np.sort(dists)
            collide = [collide[i] for i in index]


            for j,d in enumerate(dists):
                #距離がある程度近くないとダメ
                if j == 0:
                    if dists[0] > self.r_thre:
                        break
                else:
                    if d - dists[j-1] > self.r_thre:
                        break

                #最後までたどり着いたら全てひっくり返す
                if j == dists.shape[0]:
                    for k in col_ind:
                        self.bd[k].turn(c)
                else:
                    #最後に行く前に同じ色が出たらアウト
                    if collide[j].color == c:
                        break

    def draw(self,screen):
        self.sprite.draw(screen)
        for piece in self.bd:
            piece.draw(screen)
        if self.lines is not None:
            for line in self.lines:
                line.draw(screen)

        return
