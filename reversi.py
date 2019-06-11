import pygame
from mutagen.mp3 import MP3 as mp3
from pygame.locals import *
import sys
import numpy as np
import board as bd
import field as fie

def main():
    pygame.init() # 初期
    screen = pygame.display.set_mode((540, 540)) # ウィンウサイズの指定
    winrect = screen.get_rect()
    pygame.display.set_caption("reversi") # ウィンドウの上の方に出てくアレの指定
    f = fie.field((20,20))
    c = 1
    flag = 0

    while(True):
        screen.fill((122,255,122))
        colors = f.draw(screen)

        pygame.display.update() # 画面更新

        pygame.time.wait(20) # 更新間隔。多分ミリ秒

        for event in pygame.event.get(): # 終了処理
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_t:
                    print(f.test())
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                c = f.put(pos,c)


if __name__ == "__main__":
    main()
