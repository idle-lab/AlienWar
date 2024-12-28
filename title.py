import pygame.font

class Title:
    """标题类"""
    """生成标题"""
    def __init__(self,ai_game,msg,title_color=(0,0,0),title_size=60):
        # 初始化题目
        self.screen = ai_game.screen
        self.setting = ai_game.setting

        # 标题颜色
        self.title_color = title_color
        self.title_img = pygame.font.SysFont(None,title_size).render(msg,True,self.title_color,self.setting.bg_color)


    def print_title(self,pos):
        self.title_img_rect = self.title_img.get_rect()
        self.title_img_rect.center = pos
        self.screen.blit(self.title_img,self.title_img_rect)