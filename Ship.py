import pygame
from colliders import Circle_Colliders
class Ship:
    # 飞船类
    def __init__(self,ai_game):
        """初始化飞船"""
        # 屏幕初始位置信息
        self.screen = ai_game.screen

        # 飞船导入图片
        self.image = pygame.image.load("./images/ship.png")
        self.image = pygame.transform.scale(self.image,(80,80))
        self.rect = self.image.get_rect()

        self.rect.center = pygame.mouse.get_pos()

        # 飞船碰撞体
        self.colliders = Circle_Colliders(self)

    def move(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.center = mouse_pos
        self.colliders.center = mouse_pos

    def print_ship(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)





