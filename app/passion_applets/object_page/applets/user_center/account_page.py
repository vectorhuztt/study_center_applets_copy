import re

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.common import CommonPage
from conf.decorator import teststep


class SchoolPage(CommonPage):

    @teststep
    def wait_check_school_page(self):
        """学校页面检查点"""
        locator = (By.CSS_SELECTOR, '.logout')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def school_name(self):
        """学校名称"""
        locator = (By.CSS_SELECTOR, '.school-info')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def user_name(self):
        """学生名称"""
        locator = (By.CSS_SELECTOR, '.student-info .info wx-view:nth-child(1)')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def user_phone(self):
        """学生号码"""
        locator = (By.CSS_SELECTOR, '.student-info .info wx-view:nth-child(2)')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def course_num(self):
        """课程数量"""
        locator = (By.CSS_SELECTOR, '.student-info .info wx-view:nth-child(2)')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def logout_btn(self):
        """退出登录按钮"""
        locator = (By.CSS_SELECTOR, '.logout-btn')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def account_page_operate(self, student_info):
        """用户信息页面数据校对"""
        print('---- 退出登录页面----\n')
        if not self.wait_check_school_page():
            self.base_assert.except_error('未进入学校页面')
        else:
            page_school_name = self.school_name().text
            page_username = self.user_name().text
            page_phone = self.user_phone().text

            print('学校名称：', page_school_name)
            print('用户名称：', page_username)
            print('用户手机号：', page_phone, '\n')
            if student_info:
                if student_info['userphone'] != page_phone:
                    self.base_assert.except_error('页面手机号与登录时输入的手机号不一致, 登录为{}, 页面为{}'
                                                  .format(student_info['userphone'], page_phone))
                if student_info['username'] != page_username:
                    self.base_assert.except_error('页面用户名与数据库查询名称不一致, 查询名称为{}, 页面为{}'
                                                  .format(student_info['username'], page_username))

                if student_info['school_name'] != page_school_name:
                    self.base_assert.except_error('页面学校名称与数据库查询名称不一致, 查询名称为{}, 页面为{}'
                                                  .format(student_info['school_name'], page_school_name))
            self.logout_btn().click()





