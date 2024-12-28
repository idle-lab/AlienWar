# 渲染文本的类
import pygame.font

class Button:
    """UI按钮类"""
    def __init__(self,ai_game,msg,pos):
        # 初始化屏幕
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.setting = ai_game.setting

        # 设置按钮外观
        self.width, self.height = 200,50
        self.button_color = (0,135,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)

        # 设置按钮位置
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = pos
        self.msg = msg
        self._prep_msg(self.msg)

        # 按钮音效
        self.button_on_sound = pygame.mixer.Sound("./music/button_on.mp3")
        self.button_on_sound.set_volume(1)
        self.button_on_is_play = True

    def _prep_msg(self,msg):
        """设置按钮位置"""
        self.msg_img = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def print_button(self):
        # 检测鼠标位置是否在按钮范围内
        # 鼠标在按钮范围内就变红，否则就是绿色
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.button_color = self.setting.button_colo_on
            # 控制音效只播放一遍
            if self.button_on_is_play:
                self.button_on_sound.play()
                self.button_on_is_play = False
        else:
            self.button_on_is_play = True
            self.button_color = self.setting.button_colo_off

        # 渲染按钮
        self._prep_msg(self.msg)
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_img,self.msg_img_rect)