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
        self.color = c
        if self.color > 0:
            filename = os.path.join(figpath,"black.png")
        elif self.color < 0:
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

        #幅を持たせる
        dx = 6

        for p in same_color_list:
            offx = sprite.x - p.sprite.x
            offy = sprite.y - p.sprite.y

            if offx < 0:#置く方が左
                x = sprite.x-dx/2
                offx = abs(offx)
                sx = dx/2
                gx = offx+dx/2
            else:
                x = p.sprite.x
                sx = offx+dx/2
                gx = dx/2

            if offy < 0:#置く方が上
                y = sprite.y
                offy = abs(offy)
                sy = dx/2
                gy = offy+dx/2
            else:
                y = p.sprite.y
                sy = offy+dx/2
                gy = dx/2

            surf = pygame.Surface((offx+dx,offy+dx),pygame.SRCALPHA)
            pygame.draw.line(surf,(255,0,0),(sx,sy),(gx,gy),2)
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

            #衝突するものがなければスキップ
            if dists.shape[0] <= 0:
                continue

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
                if j == dists.shape[0]-1:
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
        # if self.lines is not None:
        #     for line in self.lines:
        #         line.draw(screen)
        return
