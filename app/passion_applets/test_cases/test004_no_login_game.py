import unittest

from app.passion_applets.object_page.applets.games.applet_game import AppletGamePage
from app.passion_applets.object_page.applets.home.home_page import AppletsHomePage
from app.passion_applets.object_page.applets.user_center.mine_tab_page import MineTabPage
from app.passion_applets.object_page.applets.games.result_page import ResultPage
from app.passion_applets.object_page.wechat.wechat_page import WeChatPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class AppletPlayGame(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.mine = MineTabPage()
        cls.applet_home = AppletsHomePage()
        cls.game = AppletGamePage()
        cls.result_page = ResultPage()
        cls.mine = MineTabPage()
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result, cls.applet_home.driver)
        BasePage().set_assert(cls.base_assert)
        cls.applet_home.activity_status()

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(AppletPlayGame, self).run(result)

    @testcase
    def test_play_game(self):
        """闯关游戏"""
        nickname = 0
        #  从个人中西获取用户名称
        if self.applet_home.wait_check_applets_home_page():
            self.applet_home.mine_tab().click()
            if self.mine.wait_check_mine_tab_page():
                nickname = self.mine.wechat_nickname().text
                if '暂未绑定' not in self.mine.mine_school_btn().text:
                    self.mine.logout_operate()
                self.mine.click_applet_back_btn()
                if not self.applet_home.wait_check_applets_home_page():
                    self.base_assert.except_error('点击退回按钮， 未从个人中心页面退至主页面')

        if self.applet_home.wait_check_applets_home_page():
            current_book_name = self.applet_home.current_book_name().text
            self.applet_home.start_game_btn().click()
            # 选择关卡
            if self.game.wait_check_levels_page():
                active_level = self.game.levels()
                if not active_level:
                    self.base_assert.except_error("页面不存在已解锁的关卡")
                else:
                    select_index = 0
                    select_level = active_level[select_index]
                    level_num = select_level.get_attribute('class').split()[-1].split('-')[1]
                    active_level[0].click()
                    self.game.play_games_operate(do_right=True)   # 游戏入口

                    if not self.result_page.wait_check_result_page():
                        self.base_assert.except_error('游戏结束后， 未进入结果页面')
                    else:
                        self.result_page.result_page_operate(nickname, current_book_name, level_num)
                        self.result_page.continue_game_btn().click()

                    if not self.game.wait_check_levels_page():
                        self.base_assert.except_error('点击继续闯关按钮, 未进入选择关卡页面')
                    else:
                        complete_level_class = self.game.levels()[select_index].get_attribute('class')
                        if 'complete' not in complete_level_class:
                            self.base_assert.except_error("关卡已通关， 但是关卡的状态未显示为已完成状态")
                        self.game.click_applet_back_btn()

                        if not self.applet_home.wait_check_applets_home_page():
                            self.base_assert.except_error('点击退回按钮， 未从关卡页面退至主页面')







