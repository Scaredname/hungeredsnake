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
size = width, height = 640, 480
SIZE = 20
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
        self.ran_pos = position(randint(0, 620),  randint(0, 460))
        self.islive = True
        self.draw()
    
    def draw(self):
        ran_food = pygame.Rect(self.ran_pos.x, self.ran_pos.y, SIZE, SIZE)
        pygame.draw.rect(self.screen,GREEN, ran_food)
    
    def creat(self):
        self.islive = True
        self.ran_pos = position(randint(0, 620),  randint(0, 460))

    def check(self):
        if self.islive:
            self.draw()
        else:
            self.creat()
            self.draw()

class position():
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
        self.snake_head_pos = position(randint(100,300), randint(100, 300))
        self.snake_body = []
        self.creat()
    
    def creat(self):
        self.snake_head = self.toRect(self.snake_head_pos)
        self.draw(self.snake_head, RED)
        for i in range(self.snake_len):
            snake_body = self.toRect(position(self.snake_head.x + SIZE * (i + 1), self.snake_head.y))
            self.snake_body.append(snake_body)
        for each in self.snake_body:
            self.draw(each, BLUE)
    def toRect(self,rect_pos):
        return pygame.Rect(rect_pos.x, rect_pos.y, SIZE - 1, SIZE - 1)

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
        
        # 碰壁结束游戏的判断
    def drawall(self):
        self.draw(self.snake_head, RED)
        for each in self.snake_body:
            self.draw(each, BLUE)
    
    def addbody(self):
        body_len = len(self.snake_body)
        x = self.snake_body[body_len - 2].x - self.snake_body[body_len - 1].x
        y = self.snake_body[body_len - 2].y - self.snake_body[body_len - 1].y
        addbody =  self.toRect(position(self.snake_body[body_len - 1].x - x,\
                    self.snake_body[body_len - 1].y - y))
        self.snake_body.append(addbody)
# def test(testSnake):
#     testSnake.move(position(0, 20))
#     print(testSnake.snake_body)

# 碰撞检测
def check_collision(moving_sanke, food_list):
    for each in food_list:
        if abs(moving_sanke.snake_head.x - each.ran_pos.x) < 20\
         and abs(moving_sanke.snake_head.y - each.ran_pos.y) < 20:
            each.islive = False
            moving_sanke.addbody()

def main():
    # 固定参数
    down = position(0, SIZE)
    up = position(0, -SIZE)
    left = position(-SIZE, 0)
    right = position(SIZE, 0)

    # 初始化
    pygame.init() 
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    
    mysnake = snake(screen)
    direction = choice([up, down, left, right])
    foods = []

    # 测试
    rect_pos = position(20, 30)
    # 游戏运行
    running = True
    foods.append(food(screen))
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            if direction != down:
                        direction = up
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            if direction != up:
                        direction = down
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            if direction != right:
                        direction = left
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            if direction != left:
                        direction = right
                   

        screen.fill(WHITE) #screenfill的位置很关键啊！卡了我好久。
        
        # 食物绘制,碰撞检测,增加身体
        for each in foods:
            each.check()
        check_collision(mysnake, foods)
        # 贪食蛇的绘制移动，有一个默认移动方向
        mysnake.move(direction)
        mysnake.drawall()
        
        pygame.display.flip()
        clock.tick(5)

if __name__ == "__main__":
    main() 
    

