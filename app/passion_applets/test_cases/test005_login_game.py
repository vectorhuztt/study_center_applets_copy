import time
import unittest

from app.passion_applets.object_page.applets.books.books_page import BooksPage
from app.passion_applets.object_page.applets.books.unit_page import UnitPage
from app.passion_applets.object_page.applets.games.applet_game import AppletGamePage
from app.passion_applets.object_page.applets.games.result_page import ResultPage
from app.passion_applets.object_page.applets.home.book_validate import BookDataValidatePage
from app.passion_applets.object_page.applets.home.home_page import AppletsHomePage
from app.passion_applets.object_page.applets.user_center.mine_tab_page import MineTabPage
from app.passion_applets.object_page.sql.sql_handler import SqlHandler
from app.passion_applets.object_page.wechat.wechat_page import WeChatPage
from app.passion_applets.test_data.account import Account
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class LoginReview(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.mine = MineTabPage()
        cls.applet_home = AppletsHomePage()
        cls.book_valid = BookDataValidatePage()
        cls.unit = UnitPage()
        cls.result_page = ResultPage()
        cls.result = unittest.TestResult()
        cls.game = AppletGamePage()
        cls.base_assert = ExpectingTest(cls, cls.result, cls.mine.driver)
        BasePage().set_assert(cls.base_assert)
        cls.applet_home.activity_status()

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(LoginReview, self).run(result)

    @testcase
    def test_login_review(self):
        student_info = {}
        if self.applet_home.wait_check_applets_home_page():
            self.applet_home.mine_tab().click()
            if not self.mine.wait_check_mine_tab_page():
                self.base_assert.except_error("点击我的tab按钮后， 未进入个人中心页面")
            else:
                page_school_name = self.mine.mine_school_btn()
                nickname = self.mine.wechat_nickname().text
                student_info['nickname'] = nickname
                if '暂未绑定' in page_school_name.text:
                    student_info = self.mine.login_operate()
                    if not self.mine.wait_check_mine_tab_page():
                        self.base_assert.except_error("登录后， 未重新进入个人中心页面")
                else:
                    phone = Account().account()
                    user_id, username = SqlHandler().get_login_student_id_name(phone)
                    student_info['id'] = user_id
                    student_info['username'] = username
                self.mine.click_applet_back_btn()

        print(student_info, '\n')
        if not self.applet_home.wait_check_applets_home_page():
            self.base_assert.except_error('未退回主页面')
        else:
            start_btn = self.applet_home.start_game_btn()
            if start_btn.text != '开始复习':
                self.base_assert.except_error("学生已登录, 页面按钮文本未变成开始复习")

            book_info = self.book_valid.select_one_book_and_check_data(student_info['id'], first_index=2,
                                                                       second_index=1, book_index=1)
            AppletGamePage().play_games_operate(is_review=True)
            if not self.result_page.wait_check_result_page():
                self.base_assert.except_error('游戏结束后， 未进入结果页面')
            else:

                self.result_page.result_page_operate(student_info['nickname'], book_info['book_name'],
                                                     book_info['unit_index'], is_review=True, student_id=student_info['id'])
                self.result_page.continue_game_btn().click()

            if not self.unit.wait_check_select_unit_page():
                self.base_assert.except_error('点击继续复习按钮， 未进入选择页面')
            else:
                self.unit.unit_back_btn().click()
                time.sleep(2)



