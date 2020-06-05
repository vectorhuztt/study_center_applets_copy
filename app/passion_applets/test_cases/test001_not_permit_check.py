import random
import unittest

from app.passion_applets.object_page.applets.home.book_validate import BookDataValidatePage
from app.passion_applets.object_page.applets.home.home_page import AppletsHomePage
from app.passion_applets.object_page.wechat.readd_applet import ReAddApplet
from app.passion_applets.object_page.wechat.wechat_page import WeChatPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class NotPermitCheck(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.book_valid = BookDataValidatePage()
        cls.result = unittest.TestResult()
        cls.applet_home = AppletsHomePage()
        cls.base_assert = ExpectingTest(cls, cls.result,
                                        cls.applet_home.wechat.driver)
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(NotPermitCheck, self).run(result)

    @testcase
    def test_not_permit_home_status(self):
        """从微信进入小城处理过程"""
        ReAddApplet().readd_applet_operate()
        self.applet_home.applet_util.switch_operate(self.applet_home.driver)
        self.applet_home.wechat.enter_into_applet_operate()
        if self.applet_home.wait_check_applets_home_page():
            print("进入小程序主页面")
            start_tip_image = self.applet_home.wait_check_start_tip_image()
            if not start_tip_image:
                self.base_assert.except_error("首次进入")
            else:
                start_tip_image.click()

            course_tip_image = self.applet_home.wait_check_course_tip_image()
            if not course_tip_image:
                self.base_assert.except_error("点击开始闯关提示之后, 未发现课程提示")
            else:
                course_tip_image.click()

            add_desktop_icon = self.applet_home.wait_check_add_applet_desktop()
            if not add_desktop_icon:
                self.base_assert.except_error("首次进入未发现添加小程序快捷方式提示")
            else:
                add_desktop_icon.click()

            permit_tip = self.applet_home.wait_check_permit_tip()
            if not permit_tip:
                self.base_assert.except_error("首页未显示快去授权提示")

            current_book_name = self.applet_home.current_book_name().text
            if '暂无课程' not in current_book_name:
                self.base_assert.except_error('当前学习书籍不为暂无课程')
            else:
                print('学习书籍：', current_book_name)

            current_level = self.book_valid.current_unit().text
            if current_level != '0':
                self.base_assert.except_error('当前关卡数不为0')
            else:
                print("当前关卡：", current_level)

            current_total_unit = self.book_valid.total_unit().text
            if current_total_unit != '共0关':
                self.base_assert.except_error('当前总关卡数不为0')
            else:
                print("当前总关卡数：", current_total_unit)

            studied_word_count = self.book_valid.unit_studied_word_count().text
            if studied_word_count != '0':
                self.base_assert.except_error('当前已学单词数不为0')
            else:
                print('已学单词数：', studied_word_count)

            current_unit_total_word = self.book_valid.unit_words_total_count().text
            if current_unit_total_word != '共0个':
                self.base_assert.except_error('当前关卡总共单数数不为0')
            else:
                print('当前关卡总单词数：', current_unit_total_word)

            total_studied_count = self.book_valid.book_total_studied_count().text
            if total_studied_count != '0':
                self.base_assert.except_error('累计学习单词数不为0')
            else:
                print('累计学习单词数：', total_studied_count)

            book_total_count = self.book_valid.book_total_words_count().text
            if book_total_count != '共0个':
                self.base_assert.except_error('书籍总单词数不为0')
            else:
                print('书籍总单词数：', book_total_count)

            permit_tip.click()
            self.applet_home.wechat.handle_alert_tip()
            if self.applet_home.wait_check_permit_tip():
                today_study_count = self.applet_home.today_study_count().text
                if today_study_count != '0/30词':
                    self.base_assert.except_error('今日学习任务不为0')

                else:
                    print('今日学习任务：', today_study_count)
                self.base_assert.except_error('微信授权以后， 主页面依然提示授权登录')









