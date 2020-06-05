import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.toast_find import Toast
from utils.wxapp import AppletUtil


class WeChatPage(BasePage):

    @teststep
    def wait_check_wechat_home_page(self):
        # 以微信主页微信标题为索引条件
        locator = (By.ID, self.id_type() + 'dk')
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def wait_check_applets_list_page(self):
        """下拉小程序列表页面"""
        locator = (By.XPATH, "//android.widget.TextView[@text='百项过学习']")
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def wait_check_access_alert_tip_page(self):
        """弹框提示页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[@text='申请' and @index='2']")
        return self.get_wait_check_page_ele(locator, applets=False, timeout=5)

    @teststep
    def wait_check_bind_phone_tip_page(self):
        """弹框提示页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[@text='微信帐号还没有绑定手机号']")
        return self.get_wait_check_page_ele(locator, applets=False, timeout=5)

    @teststep
    def wait_check_select_friend_page(self):
        """选择好友与群页面"""
        locator = (By.XPATH, "//android.widget.Button[@text='多选']")
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def password_input_empty_ele(self):
        """密码输入栏"""
        locator = (By.XPATH, '//android.view.View[@text="密码"]')
        return self.get_wait_check_page_ele(locator, applets=False, timeout=5)

    @teststep
    def password_input_no_empty_ele(self):
        """密码输入栏"""
        locator = (By.XPATH, '//android.view.View[contains(@text, "●")]')
        return self.get_wait_check_page_ele(locator, applets=False, timeout=5)

    @teststep
    def login_btn(self):
        """登录按钮"""
        locator = (By.XPATH, '//android.view.View[@text="登录"]')
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def wechat_back_up_btn(self):
        """微信退回按钮"""
        locator = (By.ID, self.id_type() + 'dn')
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def keyboard_num(self, num):
        """键盘上的数字"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tenpay_keyboard_{}'.format(num))
        return ele

    @teststep
    def alert_cancel_btn(self):
        """取消按钮dit"""
        locator = (By.CLASS_NAME, "android.widget.Button")
        return self.get_wait_check_page_ele(locator, applets=False, single=False)[0]

    @teststep
    def alert_confirm_btn(self):
        """弹框提示确定按钮"""
        locator = (By.CLASS_NAME, "android.widget.Button")
        return self.get_wait_check_page_ele(locator, applets=False, single=False)[1]

    @teststep
    def applet_icon(self):
        """小程序图标"""
        locator = (By.XPATH, '//android.widget.TextView[@text="百项过学习"]')
        return self.get_wait_check_page_ele(locator, single=False, applets=False)

    @teststep
    def wait_check_request_access_tip_page(self):
        """权限申请提示页面检查点"""
        locator = (By.ID, self.id_type() + 'esc')
        return self.get_wait_check_page_ele(locator, applets=False, timeout=5)

    @teststep
    def cancel_request_btn(self):
        """取消按钮"""
        locator = (By.ID, self.id_type() + 'esa')
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def allow_request_btn(self):
        """取消按钮"""
        locator = (By.ID, self.id_type() + 'esh')
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def handle_request_access(self, allow=True):
        """权限申请页面处理过程"""
        AppletUtil.switch_operate(self.driver, switch_to_app=True)
        alert_tip = self.wait_check_request_access_tip_page()
        if not alert_tip:
            print('未发现申请权限提示')
        else:
            print(alert_tip.text)
            self.allow_request_btn().click if allow else self.cancel_request_btn().click()
            time.sleep(3)
        AppletUtil.switch_operate(self.driver)

    @teststep
    def handle_alert_tip(self, allow=True):
        """微信弹框页面处理"""
        AppletUtil.switch_operate(self.driver, switch_to_app=True)
        alert_tip = self.wait_check_access_alert_tip_page() or self.wait_check_bind_phone_tip_page()
        if not alert_tip:
            print('未发现弹框提示')
        else:
            print(alert_tip.text)
            self.alert_confirm_btn().click() if allow else self.alert_cancel_btn().click()
            time.sleep(3)
            AppletUtil.switch_operate(self.driver)

    @teststeps
    def enter_into_applet_operate(self):
        """进入小程序主要步骤"""
        if self.wait_check_wechat_home_page():
            print('微信主页面')
            self.screen_swipe_down(0.5, 0.2, 0.9, 1000)
            if self.wait_check_applets_list_page():
                ele = self.applet_icon()
                if ele:
                    ele[0].click()
                    time.sleep(5)
                    AppletUtil.switch_operate(self.driver)
                else:
                    raise Exception('未发现小程序图标')

    @teststep
    def app_page_login_account(self, phone, clear_length=0):
        """登陆账号"""
        AppletUtil.switch_operate(self.driver, switch_to_app=True)
        if clear_length:
            for x in range(clear_length):
                self.keyboard_num('d').click()
        for x in (list(str(phone))):
            self.keyboard_num(x).click()
            time.sleep(0.5)
        AppletUtil.switch_operate(self.driver)

    @teststep
    def app_page_login_password(self, password, assert_text=None, is_check=False, clear_length=0):
        """登陆密码"""
        AppletUtil.switch_operate(self.driver, switch_to_app=True)
        # password_ele = self.password_input_empty_ele() or self.password_input_no_empty_ele()
        if clear_length:
            for x in range(clear_length):
                os.system("adb shell input keyevent 67")
        os.system("adb shell input text {}".format(password))
        if is_check:
            self.login_btn().click()
            if not Toast().find_toast(assert_text):
                self.base_assert.except_error("账号格式错误， 未发现提示 %s" % assert_text)
            else:
                print(assert_text, '\n')
        else:
            self.login_btn().click()
        AppletUtil.switch_operate(self.driver)