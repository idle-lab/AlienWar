import random
import pygame
from Setting import Settings
from Ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from score_board import Score_board
from title import Title
from awards import Wave
class AlienInvasion:
    """游戏主体类"""
    """处理游戏基本逻辑"""
    def __init__(self):
        # 内部各功能模块进行初始化创建及变量设置，默认调用
        pygame.init()
        pygame.mixer.init()

        # 设置时钟，控制帧率
        self.clock = pygame.time.Clock()

        # 初始化屏幕信息及游戏相关设置
        self.setting = Settings()
        self.screen = pygame.display.set_mode((self.setting.screen_width,self.setting.screen_height))
        self.screen_rect =self.screen.get_rect()

        # 存储游戏各种元素信息的集合
        self.ship = Ship(self)      # 飞船集合
        self.bullet_set = set()     # 子弹集合
        self.alien_set = set()      # 存活敌人集合
        self.alien_dead_set = set() # 死亡敌人集合    死亡敌人会存留一段时间来播放爆炸画面
        self.awards_off_set = set() # 未触发的奖励物集合
        self.awards_on_set = set()  # 触发的奖励物集合
        self.alien_time = 0         # 记录敌人生成间隔
        self.attack_time = 0        # 记录攻击间隔

        # 控制游戏状态
        self.game_active = False    # 游戏是否正在运行
        self.game_stop = False      # 游戏是否在暂停状态
        self.game_exit = False      # 游戏是否处于要退出的状态

        # 游戏界面信息
        # 开始界面UI
        center = self.screen.get_rect().center
        self.game_title = Title(self,"ALIEN WAR!!!",(135,0,0),100)

        # 导入初始背景音乐并设置声音大小
        pygame.mixer.music.load("./music/begin_bg_music.mp3")
        pygame.mixer.music.set_volume(0.2)

        # 初始化各个按键
        self.begin_button = Button(self,"Play",(center[0],center[1] - 60))
        self.rank_button = Button(self,"Ranking",(center[0],center[1] + 20))
        self.quit_button_1 = Button(self,"Quit",(center[0],center[1] + 100))
        self.return_button_1 = Button(self,"Return",(center[0],center[1] + 300))

        # 游戏时的UI
        self.stop_button = Button(self,"Continue",(center[0],center[1] - 50))
        self.quit_button_2 = Button(self,"Quit",(center[0],center[1] + 50))
        self.score_board = Score_board(self)

        # 死亡的UI
        self.dead_title = Title(self,"You Dead!",(255,0,0))
        self.again_button = Button(self,"Again",(center[0] - 150,center[1]))
        self.return_button_2 = Button(self,"Return",(center[0] + 150,center[1]))

    def reset_game(self):
        """重置游戏画面"""
        # 清楚各个集合中的元素
        self.bullet_set.clear()
        self.alien_set.clear()
        self.awards_off_set.clear()
        self.awards_off_set.clear()
        self.alien_dead_set.clear()
        self.score_board.score = 0

    def begin_UI(self):
        """开始界面渲染"""
        while not(self.game_exit or self.game_active or self.game_stop):
            # 绘制按钮
            self._update_begin_UI()

            # 响应输入
            for event in pygame.event.get():
                # 退出
                if event.type == pygame.QUIT:
                    self.game_exit = True

            # 是否在按钮范围内点击鼠标
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                # 如果在按钮范围内按下左键，就触发效果
                if self.begin_button.rect.collidepoint(mouse_pos):
                    # 导入战斗时的背景音乐
                    pygame.mixer.music.load("./music/running_bg_music.mp3")
                    self.game_active = True
                    self.reset_game()
                    # 隐藏光标
                    pygame.mouse.set_visible(False)
                # 进入rank分界面
                elif self.rank_button.rect.collidepoint(mouse_pos):
                    self.rank_UI()
                # 退出游戏
                elif self.quit_button_1.rect.collidepoint(mouse_pos):
                    self.game_exit = True

            self._update_begin()
            # 设置帧率，刷新画面
            self.clock.tick(60)
            pygame.display.flip()

    def _update_begin(self):
        self.ship.rect.center = (self.screen_rect.center[0],self.screen_rect.center[1] + 250)
        self.ship.print_ship()

        # 循环播放背景音乐
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

        # 开始界面的动画
        self.alien_time += 1.5
        if self.alien_time >= self.setting.alien_crate_speed:
            # 生成敌人
            new_alien1 = Alien(self)
            new_alien2 = Alien(self)
            # 开始界面的敌人都是从上到下移动的
            new_alien1.is_right = False
            new_alien2.is_right = False
            # 改变他们的位置，让他们避开中心的界面
            new_alien1.rect.x = random.uniform(100,300)
            new_alien2.rect.x = random.uniform(850,1100)
            self.alien_set.add(new_alien1)
            self.alien_set.add(new_alien2)
            self.alien_time = random.randint(0,self.setting.alien_crate_speed)

        # 更新敌人位置
        for alien in self.alien_set.copy():
            alien.move()
            # 超出屏幕范围的敌人就删除
            if alien.rect.y > self.screen.get_height():
                self.alien_set.remove(alien)
            else:
                alien.print_alien()


    def _update_begin_UI(self):
        # 渲染标题按钮等
        self.screen.fill(self.setting.bg_color)
        self.game_title.print_title((self.screen_rect.center[0],self.screen_rect.center[1] - 200))
        self.begin_button.print_button()
        self.rank_button.print_button()
        self.quit_button_1.print_button()

    def rank_UI(self):
        rk_UI = True
        while rk_UI:
            self._update_rank_UI()

            # 响应输入
            for event in pygame.event.get():
                # 退出
                if event.type == pygame.QUIT:
                    rk_UI = False
                    self.game_exit = True
            # 返回上一级
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if self.return_button_1.rect.collidepoint(mouse_pos):
                    break

            # 刷新图像
            pygame.display.flip()
            self.clock.tick(60)

    def _update_rank_UI(self):

        # 循环播放背景音乐
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

        # 刷新排行榜界面
        self.screen.fill(self.setting.bg_color)
        self.score_board.print_history_score()
        self.return_button_1.print_button()

    def run_game(self):
        """游戏主体"""
        while  (self.game_active or self.game_stop) and not self.game_exit:
            # 游戏运行响应输入
            self._check_events()
            # 绘制新一帧画面
            self._update_screen()

            # 刷新画面缓冲区
            pygame.display.flip()
            # 保证该循环保持在 60fps
            self.clock.tick(60)

    def _check_events(self):
        """检查键盘鼠标输入"""
        for event in pygame.event.get():
            # 点击叉号退出
            if event.type == pygame.QUIT:
                self.game_exit = True
            elif event.type == pygame.KEYDOWN:
                self._check_key(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse()

    def _check_key(self,event):
        """响应键盘输入"""
        # 按q直接退出
        if event.key == pygame.K_q:
            self.game_exit = True
        # 按s暂停
        elif event.key == pygame.K_s:
            self.game_active = False
            self.game_stop = True
            pygame.mouse.set_visible(True)

    def _check_mouse(self):
        """响应鼠标输入"""
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            # 继续游戏
            if self.stop_button.rect.collidepoint(mouse_pos):
                self.game_active = True
                self.game_stop = False
                pygame.mouse.set_visible(False)
            # 退出到主界面
            elif self.quit_button_2.rect.collidepoint(mouse_pos):
                self.game_active = False
                self.game_stop = False
                self.reset_game()
                # 退回主界面时，重新加载背景音乐
                pygame.mixer.music.load("./music/begin_bg_music.mp3")

    def _update_screen(self):
        """更新画面"""
        # 渲染背景和分数UI
        self.screen.fill(self.setting.bg_color)
        self.score_board.print_score()

        # 循环播放战斗时的背景音乐
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

        # 更新各个元素位置
        self._update_ship()
        self._update_bullet()
        self._update_alien()
        self._update_dead_alien()
        self._update_off_awards()
        self._update_on_awards()

        # 暂停时打印暂停按钮
        if self.game_stop:
            self.stop_button.print_button()
            self.quit_button_2.print_button()

    def _update_ship(self):
        """更新玩家飞船位置"""
        self.ship.print_ship()
        # 飞船跟随鼠标移动
        if self.game_active:
            self.ship.move()
            self.attack_time += min(1 + self.score_board.score / 500,10)
            if self.attack_time >= self.setting.attack_gap:
                self.bullet_set.add(Bullet(self))
                self.attack_time = 0

            # 碰撞体接触到敌人时玩家死亡
            for alien in self.alien_set:
                if self.ship.colliders.check_Colliders(alien.colliders):
                    self.dead_UI()
                    break

    def _update_bullet(self):
        """更新子弹位置"""
        for bullet in self.bullet_set.copy():
            if self.game_active:
                bullet.move()
            # 超出屏幕范围的子弹就删除
            if bullet.rect.y <= 0:
                self.bullet_set.remove(bullet)
                continue
            bullet.print_bullet()
            for alien in self.alien_set.copy():
                # 判断子弹是否打中敌人
                if bullet.colliders.check_Colliders(alien.colliders):
                    self.bullet_set.remove(bullet)
                    alien.dead(self)
                    break

    def _update_alien(self):
        """更新敌人位置"""
        # 游戏暂停时不生成敌人
        if self.game_active:
            # 控制敌人创建速度
            # 根据得分逐渐增加敌人生成速率
            self.alien_time += (1 + self.score_board.score / 500)
            if self.alien_time >= self.setting.alien_crate_speed:
                # 生成敌人
                self.alien_set.add(Alien(self))
                self.alien_time = random.randint(0,self.setting.alien_crate_speed)

        # 更新敌人位置
        for alien in self.alien_set.copy():
            if self.game_active:
                alien.move()
            # 超出屏幕范围的敌人就删除
            if alien.rect.y > self.screen.get_height() or alien.rect.x > self.screen.get_width():
                self.alien_set.remove(alien)
            else:
                alien.print_alien()

    def _update_off_awards(self):
        """更新未激活奖励物品的位置"""
        for award in self.awards_off_set.copy():
            if self.game_active:
                award.move()
            if self.ship.colliders.check_Colliders(award.colliders):
                self.awards_off_set.remove(award)
                self.awards_on_set.add(award)
            # 超出屏幕范围的直接删除
            if award.rect.y > self.screen.get_height():
                self.awards_off_set.remove(award)
            else:
                award.print_wave_img()

    def _update_on_awards(self):
        """更新冲击波范围"""
        for award in self.awards_on_set.copy():
            if self.game_active:
                award.update(self)
            if award.wave_radius_outside > self.setting.screen_width:
                self.awards_on_set.remove(award)

    def _update_dead_alien(self):
        """更新敌人死亡动画"""
        for alien,t in self.alien_dead_set.copy():
            # 每个死亡敌人存活10个循环，来播放死亡动画
            self.alien_dead_set.remove((alien,t))
            t += 1
            if t < 10:
                self.alien_dead_set.add((alien,t))
            # 如果该敌人包含奖励，就创建一个奖励物加入到集合中
            elif alien.is_award:
                self.awards_off_set.add(Wave(self,alien))
            if t >= 7:
                alien.img = alien.dead_img2
            alien.print_alien()


    def dead_UI(self):
        # 显示光标
        pygame.mouse.set_visible(True)
        self.score_board.get_score()
        while True:
            # 更新UI画面
            self._update_dead_UI()
            # 响应输入
            if not self._check_dead_UI():
                break
            # 刷新画面缓冲区
            pygame.display.flip()
            # 保证该循环保持在 60fps
            self.clock.tick(60)

    def _update_dead_UI(self):
        # 打印死亡标题
        self.dead_title.print_title((self.screen_rect.center[0], self.screen_rect.center[1] - 100))
        # 打印按钮
        self.again_button.print_button()
        self.return_button_2.print_button()

    def _check_dead_UI(self):
        # 响应输入
        for event in pygame.event.get():
            # 点叉号退出
            if event.type == pygame.QUIT:
                self.game_exit = True
                return False
            # 有鼠标按下的操作
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    # 按继续键，就重新开始
                    if self.again_button.rect.collidepoint(mouse_pos):
                        self.reset_game()
                        pygame.mouse.set_visible(False)
                        return False
                    # 按返回键返回到主界面
                    elif self.return_button_2.rect.collidepoint(mouse_pos):
                        self.game_stop = False
                        self.game_active = False
                        # 切换成开始界面的背景音乐
                        pygame.mixer.music.load("./music/begin_bg_music.mp3")

                        self.reset_game()
                        return False
        return True


    def store_data(self):
        """将分数记录存储到文件中"""
        """只记录前5的分数"""
        self.score_board.get_score()
        score_text = ''
        for score in self.score_board.history_score_ranking:
            score_text += str(score) + '\n'
        self.score_board.history_score.write_text(score_text)


if __name__ == '__main__':
    # 初始化
    ai = AlienInvasion()

    while not ai.game_exit:
        ai.begin_UI()
        ai.run_game()

    ai.store_data()