import pygame
from pathlib import Path
import pygame.font
from title import Title

class Score_board:
    def __init__(self,ai_game):

        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.screen_rect = ai_game.screen.get_rect() ##窗口

        # 当前分数和历史分数记录
        self.score = 0
        self.history_score = Path("./data/history score.txt")
        self.history_score_ranking = []

        # 读取历史分数
        self.history_score_ranking = list(map(int,self.history_score.read_text().split()))

        # 字体大小风格颜色设置
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,60) ##渲染字体

        # 排行榜标题
        self.No_Ranking = Title(ai_game,"No Ranking")
        self.Ranking = Title(ai_game,"Ranking")

    def _prep_score(self,score):
        score_str = str(score)
        self.score_img = self.font.render(score_str,True,self.text_color,self.setting.bg_color)

        # 在右上角显示当前分数
        self.score_img_rect = self.score_img.get_rect()
        self.score_img_rect.right = self.screen_rect.right - 20
        self.score_img_rect.top = 40

    def print_score(self):
        self._prep_score(self.score)
        self.screen.blit(self.score_img,self.score_img_rect)

    def add_score(self):
        self.score += self.setting.alien_points

    def get_score(self):
        """将当前没记录的分数记录到排名中去"""
        if self.score:
            self.history_score_ranking.append(self.score)
            self.score = 0
        self.history_score_ranking.sort(reverse=True) #排序
        if len(self.history_score_ranking) > 5:
            self.history_score_ranking = self.history_score_ranking[:5] #取前五

    def print_history_score(self):
        self.get_score()
        # 打印排行榜标题
        self.Ranking.print_title((self.screen_rect.center[0],self.screen_rect.center[1] - 200))
        # 记录不为空
        if self.history_score_ranking:
            # 将分数记录按大小顺序绘制到屏幕上去
            for i,score in enumerate(self.history_score_ranking):
                self._prep_score(score)
                self.score_img_rect.center = (600,200 + (i + 1) * 60) #居中
                self.screen.blit(self.score_img,self.score_img_rect)
        # 无记录时输出提示
        else:
            self.No_Ranking.print_title(self.screen_rect.center)

