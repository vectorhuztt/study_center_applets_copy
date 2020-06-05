import time

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.common import CommonPage
from app.passion_applets.test_data.phone_valid import phone_data
from conf.decorator import teststep
from utils.date_valid import ValidDate


class ApplySchoolPage(CommonPage):

    @teststep
    def wait_check_apply_no_data_page(self):
        """暂无匹配结果"""
        locator = (By.CSS_SELECTOR, '.no-data')
        return self.get_wait_check_page_ele(locator, timeout=5)

    @teststep
    def wait_check_apply_has_school_page(self):
        """存在推荐学校的页面检查点"""
        locator = (By.CSS_SELECTOR, '.school')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_qrcode_img_page(self):
        """学校二维码页面检查点"""
        locator = (By.CSS_SELECTOR, '.dialog--fadeIn .dialog--dialog-wrapper')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_send_phone_apply_page(self):
        """输入手机号申请页面检查点"""
        locator = (By.CSS_SELECTOR, '.apply-info')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def recommend_school_name(self):
        """推荐学校名称"""
        locator = (By.CSS_SELECTOR, '.school-name')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def qrcode_icon(self):
        """推荐学校二维码"""
        locator = (By.CSS_SELECTOR, '.qrcode')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def close_qrcode_btn(self):
        """关闭学校二维码"""
        locator = (By.CSS_SELECTOR, '.dialog--fadeIn .dialog--dialog-wrapper .dialog--close1')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def location_info(self):
        """推荐学校的距离"""
        locator = (By.CSS_SELECTOR, '.location-info')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def join_btn(self):
        """申请加入按钮"""
        locator = (By.CSS_SELECTOR, '.join-btn')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def apply_success_info(self):
        """申请成功页面"""
        locator = (By.CSS_SELECTOR, '.dialog--fadeIn .success-info')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def dialog_confirm_btn(self):
        """弹框确定按钮"""
        locator = (By.CSS_SELECTOR, '.dialog--fadeIn .dialog--ok-btn')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def dialog_close_btn(self):
        """弹框右上角关闭按钮"""
        locator = (By.CSS_SELECTOR, '.dialog--fadeIn .dialog--close')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def precautions_info(self):
        """注意事项文本"""
        locator = (By.CSS_SELECTOR, '.hint')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def phone_input(self):
        """手机号输入框"""
        locator = (By.CSS_SELECTOR, '.input-wrapper div[parse-text-content]')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def send_apply_btn(self):
        """发送申请按钮"""
        locator = (By.CSS_SELECTOR, '.dialog--fadeIn .dialog--ok-btn')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def apply_school_operate(self, student_id):
        """申请学校操作"""
        print('---- 申请学校页面 ----\n')
        if self.wait_check_apply_no_data_page():
            print('暂无匹配学校')
            self.click_applet_back_btn()
            return False

        if self.wait_check_apply_has_school_page():
            print('学校名称：', self.recommend_school_name().text)
            school_position = self.location_info().text
            distance = ValidDate.get_single_num_from_text(school_position)
            if distance > 3.1:
                self.base_assert.except_error('推荐学校距离大于3km')
            self.qrcode_icon().click()
            if not self.wait_check_qrcode_img_page():
                self.base_assert.except_error('点击学校二维码图标未出现二维码图片')
            else:
                self.close_qrcode_btn().click()
                time.sleep(3)

            self.join_btn().click()
            if not self.wait_check_send_phone_apply_page():
                self.base_assert.except_error('点击申请加入按钮， 未出现申请页面')

            map_school_id = self.sql_handler.get_student_map_school(student_id)
            is_applied = self.sql_handler.get_student_school_apply_status(student_id, map_school_id)
            print(is_applied)
            if is_applied:
                self.phone_input().click()
                self.wechat.app_page_login_account(phone_data[-1])
                self.dialog_confirm_btn().click()
                if self.apply_success_info():
                    self.base_assert.except_error('该学校已经申请过，点击申请依然可以申请')
                    self.dialog_confirm_btn().click()
                else:
                    self.dialog_close_btn().click()
            else:
                for i, x in enumerate(phone_data):
                    print('输入手机号：', x)
                    phone_input = self.phone_input()
                    content_length = len(list(phone_data[i])) if i != 0 else 0
                    phone_input.click()
                    self.wechat.app_page_login_account(phone_data[i], content_length)
                    self.dialog_confirm_btn().click()
                    success_page = self.apply_success_info()
                    if i != len(phone_data) - 1:
                        if success_page:
                            self.base_assert.except_error('手机格式不正确， 却依然可以申请成功， 手机号：%s' % x)
                            self.dialog_confirm_btn().click()
                    else:
                        if not success_page:
                            self.base_assert.except_error('该学校未申请，输入正确手机号未申请成功, 手机号： %s' % x)
                        else:
                            print(success_page.text, '\n')
                            self.dialog_confirm_btn().click()
            print(self.precautions_info().text)
            self.click_applet_back_btn()
            return True
