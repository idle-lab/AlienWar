import pygame
from colliders import Circle_Colliders

class Wave:
    def __init__(self,ai_game,alien):

        self.screen = ai_game.screen
        self.setting = ai_game.setting

        # 导入冲击波图片
        self.img = pygame.image.load("./images/wave.png")
        self.img = pygame.transform.scale(self.img,(self.setting.award_width,self.setting.award_height))
        self.rect = alien.rect
        self.y = self.rect.y

        # 冲击波碰撞体
        self.colliders = Circle_Colliders(self)

        # 冲击波扩散速度
        self.wave_speed = 10
        # 冲击波半径
        self.wave_radius_outside = 10
        self.wave_radius_inside = 1

    def move(self):
        self.y += self.setting.award_speed
        self.rect.y = self.y
        self.colliders.center = self.rect.center

    def print_wave_img(self):
        self.screen.blit(self.img,self.rect)


    def update(self,ai_game):
        """扩散冲击波"""
        pygame.draw.circle(self.screen,(99,155,255),self.rect.center,self.wave_radius_outside,10)
        pygame.draw.circle(self.screen,(95,205,228),self.rect.center,self.wave_radius_inside,5)
        self.wave_radius_inside += self.wave_speed
        self.wave_radius_outside += self.wave_speed
        self.colliders.radius = self.wave_radius_outside
        for alien in ai_game.alien_set.copy():
            if self.colliders.check_Colliders(alien.colliders):
                alien.is_award = False
                alien.dead(ai_game)


