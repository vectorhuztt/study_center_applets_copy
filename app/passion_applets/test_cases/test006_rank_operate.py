import unittest

from app.passion_applets.object_page.applets.home.home_page import AppletsHomePage
from app.passion_applets.object_page.applets.rank.rank_page import RankPage
from app.passion_applets.object_page.applets.user_center.mine_tab_page import MineTabPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class RankOperate(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.applet_home = AppletsHomePage()
        cls.rank = RankPage()
        cls.mine = MineTabPage()
        cls.base_assert = ExpectingTest(cls, cls.result,
                                        cls.applet_home.wechat.driver)
        BasePage().set_assert(cls.base_assert)
        cls.applet_home.wechat.enter_into_applet_operate()

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super().run(result)

    @testcase
    def test_rank_data_page(self):
        user_nickname = ''
        if self.applet_home.wait_check_applets_home_page():
            # 进入个人中心获取当前用户昵称
            self.applet_home.mine_tab().click()
            if not self.mine.wait_check_mine_tab_page():
                self.base_assert.except_error("点击我的tab按钮后， 未进入个人中心页面")
            else:
                user_nickname = self.mine.wechat_nickname().text
                self.mine.click_applet_back_btn()

        if self.applet_home.wait_check_applets_home_page():
            # 排行榜页面数据校验
            self.applet_home.rank_tab().click()
            if self.rank.wait_check_rank_page():
                self.rank.rank_data_check_operate(user_nickname)