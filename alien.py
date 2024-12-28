import random
import pygame
from colliders import Circle_Colliders
class Alien:
    """敌人类"""
    def __init__(self,ai_game):
        # 初始化屏幕
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.score_board = ai_game.score_board

        # 导入敌人图像
        self.img = pygame.image.load("./images/alien.bmp")
        # 导入敌人死亡效果
        self.dead_img = pygame.image.load("./images/boom.png")
        self.dead_img = pygame.transform.scale(self.dead_img,(50,50))
        self.dead_img2 = pygame.image.load("./images/boom2.png")
        self.dead_img2 = pygame.transform.scale(self.dead_img2,(30,30))

        # 设定敌人出生位置
        self.rect = self.img.get_rect()
        self.rect.y = 0
        self.rect.x = random.uniform(70,ai_game.screen.get_width() - 100)
        self.y = self.rect.y
        self.x = self.rect.x

        # 设定敌人碰撞体
        self.colliders = Circle_Colliders(self)

        # 敌人死亡音效
        self.dead_sound = pygame.mixer.Sound("./music/alien_dead.mp3")

        # 敌人是否含有奖励物品
        self.is_award = (random.uniform(0,1) <= self.setting.award_probability)

        # 敌人飞行方向
        self.is_right = (random.uniform(0,1) <= self.setting.alien_is_right)
        if self.is_right:
            self.rect.y = random.uniform(0,ai_game.screen.get_height())
            self.rect.x = 0
            self.x = 0

    def move(self):
        """移动敌人"""
        # 根据的得分增加敌人移动速度
        alien_v = min(self.setting.alien_speed + self.score_board.score / 500,10.0)
        if self.is_right:
            self.x += alien_v
            self.rect.x = self.x
        else:
            self.y += alien_v
            self.rect.y = self.y
        self.colliders.center = self.rect.center

    def print_alien(self):
        """绘制敌人"""
        self.screen.blit(self.img,self.rect)

    def dead(self,ai_game):
        """敌人死亡"""
        self.dead_sound.play()
        self.img = self.dead_img
        ai_game.alien_set.remove(self)
        ai_game.alien_dead_set.add((self, 0))
        ai_game.score_board.add_score()

