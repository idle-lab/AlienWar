import pygame
from colliders import Circle_Colliders

class Bullet:
    """子弹类"""
    def __init__(self,ai_game):

        # 初始化
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.color = ai_game.setting.bullet_color

        # 在飞船位置生成子弹
        self.img = pygame.image.load("./images/bullet.png")
        # 缩放图片
        self.img = pygame.transform.scale(self.img,(self.setting.bullet_width,self.setting.bullet_height))
        self.rect = self.img.get_rect()
        self.rect.midtop  = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

        # 初始化碰撞体
        self.colliders = Circle_Colliders(self)



    def move(self):
        """移动子弹"""
        self.y -= self.setting.bullet_speed
        self.rect.y = self.y
        self.colliders.center = self.rect.center

    def print_bullet(self):
        """绘制子弹"""
        self.screen.blit(self.img,self.rect)






