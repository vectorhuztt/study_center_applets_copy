import unittest

from app.passion_applets.object_page.applets.books.books_page import BooksPage
from app.passion_applets.object_page.applets.home.book_validate import BookDataValidatePage
from app.passion_applets.object_page.applets.home.home_page import AppletsHomePage
from app.passion_applets.object_page.applets.user_center.mine_tab_page import MineTabPage
from app.passion_applets.object_page.sql.sql_handler import SqlHandler
from app.passion_applets.object_page.wechat.wechat_page import WeChatPage
from app.passion_applets.test_data.account import Account
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class HasPermittedStatus(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.wechat = WeChatPage()
        cls.applet_home = AppletsHomePage()
        cls.mine = MineTabPage()
        cls.sql_handler = SqlHandler()
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result, cls.wechat.driver)
        BasePage().set_assert(cls.base_assert)
        cls.applet_home.activity_status()

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(HasPermittedStatus, self).run(result)

    @testcase
    def test_select_book(self):
        """从微信进入小程序处理过程"""
        if self.applet_home.wait_check_applets_home_page():
            user_id = 0
            is_login = False
            self.applet_home.mine_tab().click()
            if not self.mine.wait_check_mine_tab_page():
                self.base_assert.except_error("点击我的tab按钮后， 未进入个人中心页面")
            else:
                username = self.mine.wechat_nickname().text
                page_school_name = self.mine.mine_school_btn()
                if '暂未绑定' in page_school_name.text:
                    user_id = self.sql_handler.get_wechat_user_id(username)
                else:
                    phone = Account().account()
                    user_id = self.sql_handler.get_login_student_id_name(phone)
                    is_login = False
                print('学生id：', user_id)
                self.applet_home.click_applet_back_btn()

            if not self.applet_home.wait_check_applets_home_page():
                self.base_assert.except_error("从个人中心退回， 未进入主页面")
            else:
                self.applet_home.current_book_name().click()
                self.wechat.handle_request_access()
                # 随机选择一本书
                book_info = BooksPage().select_label_books_operate()
                BookDataValidatePage().check_book_data(user_id, book_info, is_login)










