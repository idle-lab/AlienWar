import pygame
class Settings:
    """基础设置类"""

    def __init__(self):
        # 规定初始化信息

        # 屏幕设置
        self.screen_width = 1200            # 屏幕宽度
        self.screen_height = 800            # 屏幕长度
        self.bg_color = (230,230,230)       # 背景颜色

        # 子弹设置
        self.attack_gap = 40.0              # 攻击间隔时间
        self.bullet_speed = 7.0             # 子弹速度
        self.bullet_width = 15              # 子弹宽度
        self.bullet_height = 15             # 子弹长度
        self.bullet_color = (100,60,60)     # 子弹颜色

        # 敌人设置
        self.alien_speed = 3.0

        # 敌人移动速度
        self.alien_crate_speed = 100.0      # 敌人生成速度
        self.alien_points = 10              # 击杀敌人得分
        self.alien_is_right = 0.5           # 敌人横着走的概率

        # 按钮设置
        self.button_colo_on = (135,0,0)     # 鼠标在按钮上时的按钮颜色
        self.button_colo_off = (0,135,0)    # 鼠标不在按钮上时的按钮颜色

        # 奖品大小
        self.award_width = 25               # 奖励物宽
        self.award_height = 25              # 奖励物长
        self.award_speed = 3.0              # 奖励物移动速度
        self.award_probability = 0.1        # 奖励物品生成几率

        # 设置窗口标题
        pygame.display.set_caption("Alien War!!!")
        pygame.display.set_icon(pygame.image.load("./Alien War.ico"))

