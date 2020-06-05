import datetime
import time

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.common import CommonPage
from conf.decorator import teststep
from utils.date_valid import ValidDate
from utils.wxapp import AppletUtil


class ResultPage(CommonPage):

    @teststep
    def wait_check_result_page(self):
        """结果页面检查点"""
        locator = (By.CSS_SELECTOR, '.results')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_report_page(self):
        """生成的海报页面检查点"""
        locator = (By.CSS_SELECTOR, '.share-image')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_save_success_page(self):
        """保存成功 页面检查点"""
        locator = (By.CSS_SELECTOR, '.dialog--dialog.dialog--fadeIn')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def nickname(self):
        """用户昵称"""
        locator = (By.CSS_SELECTOR, '.nickname')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def book_level_info(self):
        """书籍、关卡信息"""
        locator = (By.CSS_SELECTOR, '.message .highlighted')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def page_date(self):
        """日期时间"""
        locator = (By.CSS_SELECTOR, '.date')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def data_counter(self):
        """数据统计面板"""
        locator = (By.CSS_SELECTOR, '.dashboard-item .value')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def share_btn(self):
        """分享按钮"""
        locator = (By.CSS_SELECTOR, '.buttons .van-button[open-type]')
        return self.get_wait_check_page_ele(locator, timeout=5)

    @teststep
    def generate_report_btn(self):
        """生成海报按钮"""
        locator = (By.CSS_SELECTOR, '.buttons .van-button:nth-child(2)')
        return self.get_wait_check_page_ele(locator, timeout=5)

    @teststep
    def share_friend_btn(self):
        """分享给好友"""
        locator = (By.CSS_SELECTOR, ".share-buttons .button:nth-child(1)")
        return self.get_wait_check_page_ele(locator, timeout=5)

    @teststep
    def share_and_generate_report_btn(self):
        """生成海报并分享"""
        locator = (By.CSS_SELECTOR, ".share-buttons .button:nth-child(2)")
        return self.get_wait_check_page_ele(locator, timeout=5)

    @teststep
    def continue_game_btn(self):
        """继续闯关按钮"""
        locator = (By.CSS_SELECTOR, '.buttons .van-button-info')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def save_img_btn(self):
        """生成海报按钮"""
        locator = (By.CSS_SELECTOR, '.share-wrapper .button-wrapper wx-view:nth-child(1)')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def cancel_img_btn(self):
        """取消按钮"""
        locator = (By.CSS_SELECTOR, '.share-wrapper .button-wrapper wx-view:nth-child(2)')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def success_info(self):
        """保存信息成功"""
        locator = (By.CSS_SELECTOR, '.dialog--dialog.dialog--fadeIn .success-info')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def success_ok_btn(self):
        """知道了按钮"""
        locator = (By.CSS_SELECTOR, '.dialog--dialog.dialog--fadeIn .dialog--ok-btn')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def share_image_operate(self):
        share_btn = self.share_friend_btn() or self.share_btn()
        share_btn.click()
        time.sleep(2)
        AppletUtil.switch_operate(self.driver, switch_to_app=True)
        if not self.wechat.wait_check_select_friend_page():
            self.base_assert.except_error('点击分享给好友按钮， 未进入微信选择好友页面')
        self.wechat.wechat_back_up_btn().click()
        AppletUtil.switch_operate(self.driver)
        # 生成报告按钮检验
        generate_report_btn = self.generate_report_btn() or self.share_and_generate_report_btn()
        generate_report_btn.click()
        if not self.wait_check_report_page():
            self.base_assert.except_error('点击生成海报按钮， 未出现海报页面')
        else:
            self.save_img_btn().click()
            self.wechat.handle_request_access()
            if not self.wait_check_save_success_page():
                self.base_assert.except_error('点击保存并分享按钮, 未弹出保存成功信息')
            else:
                print(self.success_info().text)
                self.success_ok_btn().click()

    @teststep
    def date_check_operate(self):
        """日期时间数据校对"""
        date = datetime.datetime.now()
        week_day_index = date.weekday()
        moth = ValidDate.reform_date(date.month)
        day = ValidDate.reform_date(date.day)
        hour = ValidDate.reform_date(date.hour)
        minute = [ValidDate.reform_date(date.minute), ValidDate.reform_date(date.minute-1)]

        page_date_info = self.page_date().text.split()
        page_week = page_date_info[0]
        page_date = page_date_info[1]
        page_time = page_date_info[2]

        if ('星期' + ValidDate.WEEK_NAME[week_day_index]) != page_week:
            self.base_assert.except_error('结果页中日期中的星期数与当前时间不一致')

        if (str(moth) + '月' + str(day) + '日') != page_date:
            self.base_assert.except_error('结果页的日期中的日期与当前时间不一致')

        if page_time not in [hour+":" + x for x in minute]:
            self.base_assert.except_error('结果页时间与当前提交时间不一致')

    @teststep
    def result_page_operate(self, nickname, book_name, level_num=None, is_review=False, student_id=None):
        """
        结果页处理过程
        :param nickname: 学生昵称
        :param book_name: 图书名称
        :param level_num: 选择的图书关卡
        :param is_review: 是否是复习状态
        :param student_id: 学生id
        """
        if self.wait_check_result_page():
            page_username = self.nickname().text
            page_book_name = self.book_level_info()[0].text
            page_book_num = self.book_level_info()[1].text
            if nickname != page_username:
                self.base_assert.except_error('结果页的用户昵称与微信名称不一致, 页面为%s， 微信名为%s' % (page_username, nickname))

            if book_name != page_book_name:
                self.base_assert.except_error('结果页显示的书籍名称与所选书籍名称不一致, 页面为%s, 选择书籍名为%s' %
                                              (page_book_name, book_name))

            if is_review:
                check_review_num = str(self.sql_handler.get_book_today_review_count(student_id))
                if check_review_num != page_book_num:
                    self.base_assert.except_error('结果页显示的今日复习数与数据库查询的不一致, 页面为 %s, 查询为 %s' %
                                                  (page_book_num, check_review_num))
            else:

                if level_num != page_book_num:
                    self.base_assert.except_error('结果页的关卡数与当前通过的关卡数不一致, 页面为 %s, 实际为%s' %
                                                  (page_book_num, level_num))
            # 时间数据校验
            self.date_check_operate()
            # 分享按钮校验
            self.share_image_operate()
            if not self.wait_check_result_page():
                self.base_assert.except_error('点击确定按钮未重新进入报告页面')
            time.sleep(3)
        



