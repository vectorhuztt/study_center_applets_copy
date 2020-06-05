import unittest
from app.passion_applets.object_page.applets.home.home_page import AppletsHomePage
from app.passion_applets.object_page.applets.user_center.mine_tab_page import MineTabPage
from app.passion_applets.object_page.applets.user_center.account_page import SchoolPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class UserCenter(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.mine = MineTabPage()
        cls.applet_home = AppletsHomePage()
        cls.school = SchoolPage()
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result, cls.mine.driver)
        BasePage().set_assert(cls.base_assert)
        cls.applet_home.activity_status()

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(UserCenter, self).run(result)

    @testcase
    def test_user_center(self):
        """测试在我的页面绑定手机号或者绑定学生端账号"""
        if self.applet_home.wait_check_applets_home_page():
            current_book_name = self.applet_home.current_book_name().text
            self.applet_home.mine_tab().click()
            if self.mine.wait_check_mine_tab_page():
                mine_study_book = self.mine.current_study_book().text
                if current_book_name != mine_study_book:
                    self.base_assert.except_error('当前学习课程与主页面的课程名称不一致')
                else:
                    print('当前学习课程：', mine_study_book)

                #  重新选择书籍
                # self.mine.change_book_operate()
                # 校验学校是否已经登录, 有则退出登录
                page_school_name = self.mine.mine_school_btn()
                if '暂未绑定' not in page_school_name.text:
                    self.mine.bind_student_btn().click()
                    if self.school.wait_check_school_page():
                        self.school.logout_btn().click()
                # 学生登录
                student_info = self.mine.login_operate(is_check=True)
                # 退出登录
                self.mine.logout_operate(student_info)
                # # 申请学校操作
                self.mine.apply_school_operate()




























