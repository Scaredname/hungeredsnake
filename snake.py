"""
基于pygame的贪吃蛇游戏
逻辑梳理
食物类，有随机坐标的方块，加入碰撞属性
贪吃蛇有一个蛇头，和蛇身。移动是蛇头先走，每一块蛇身依次覆盖上一个蛇身的位置。
贪吃蛇每吃一个食物就增加1长度的蛇身
当蛇头碰到边界时或者蛇身时游戏结束
有最高分时
"""
# !python3
# coding=utf-8 

import pygame
import sys
from pygame.locals import *
from random import *

# 常量
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class food(pygame.sprite.Sprite):
    """
    食物类
    """
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.ran_pos = positon(randint(0, 620),  randint(0, 460))
        self.creat()
    
    def creat(self):
        ran_food = pygame.Rect(self.ran_pos.x, self.ran_pos.y, 20, 20)
        pygame.draw.rect(self.screen,BLUE, ran_food)

class positon():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class snake(pygame.sprite.Sprite):
    """
    贪吃蛇类
    """
    def __init__(self, screen, snake_len = 2):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.snake_len = snake_len
        self.snake_body = []
        self.creat()
    
    def creat(self):
        self.snake_head = self.toRect(positon(randint(100,300), randint(100, 300)))
        self.draw(self.snake_head, RED)
        for i in range(self.snake_len):
            snake_body = self.toRect(positon(self.snake_head.x + 20 * (i + 1), self.snake_head.y))
            self.snake_body.append(snake_body)
        for each in self.snake_body:
            self.draw(each, BLUE)
    def toRect(self,rect_pos):
        return pygame.Rect(rect_pos.x, rect_pos.y, 19, 19)

    def draw(self, rect, color):
        pygame.draw.rect(self.screen, color, rect)

    def move(self, direction):
        
        for i in range(len(self.snake_body) - 1, -1, -1):
            if i == 0:
                self.snake_body[i].x = self.snake_head.x
                self.snake_body[i].y = self.snake_head.y
            else:
                self.snake_body[i].x = self.snake_body[i - 1].x
                self.snake_body[i].y = self.snake_body[i - 1].y
        
        self.snake_head.x += direction.x
        self.snake_head.y += direction.y
        
        # 少一个碰壁结束游戏的判断
    def drawall(self):
        self.draw(self.snake_head, RED)
        for each in self.snake_body:
            self.draw(each, BLUE)


def test(testSnake):
    testSnake.move(positon(0, 20))
    print(testSnake.snake_body)
    

def main():
    # 固定参数
    size = width, height = 640, 480

    # 初始化
    pygame.init() 
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    
    mysnake = snake(screen)

    # 测试
    rect_pos = positon(20, 30)
    # 游戏运行
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        
        if event.type == KEYDOWN:
            if event.key == K_w:
                test(mysnake)
                rect_pos.x += 5
                rect_pos.y += 5

        screen.fill(WHITE) #screenfill的位置很关键啊！卡了我好久。
        mysnake.drawall()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main() 
    

