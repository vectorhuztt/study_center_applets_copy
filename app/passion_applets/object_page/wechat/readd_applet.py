from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class ReAddApplet(BasePage):

    @teststep
    def wait_check_find_page(self):
        """发现页面"""
        locator = (By.XPATH, "//android.widget.TextView[@text='小程序' and contains(@resource-id, 'android:id/title')]")
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def wait_check_test_applet_page(self):
        """测试小程序页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[@text='小程序' and contains(@resource-id, 'android:id/title')]")
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def wait_check_applet_list_page(self):
        """小程序列表页面"""
        locator = (By.XPATH, "//android.widget.TextView[@text='附近的小程序']")
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def wait_check_search_page(self):
        """搜索内容页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[@text='搜索指定内容']")
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def discovery_tab(self):
        locator = (By.XPATH, "//android.widget.TextView[@text='发现' and contains"
                             "(@resource-id, 'com.tencent.mm:id/cns')]")
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def find_icon(self):
        """搜索按钮"""
        locator = (By.ACCESSIBLITY_ID, "搜索")
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def search_input_ele(self):
        """搜索输入框"""
        locator = (By.XPATH, "//android.widget.EditText[@text='搜索' and @resource-id='com.tencent.mm:id/bhn']")
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def wait_check_test_applet(self, var):
        """百项过小程序"""
        locator = (By.XPATH, "//android.widget.TextView[@text='{}']".format(var))
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def search_applet(self):
        """搜一搜"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '搜一搜')]")
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def wait_check_search_applet_result_page(self, var):
        locator = (By.XPATH, "//android.view.View[@text='{} - 小程序']".format(var))
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def delete_applet(self):
        """删除小程序"""
        locator = (By.XPATH, "//android.widget.TextView[@text='删除']")
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def find_test_applet(self, var):
        """已查询到的小程序"""
        locator = (By.XPATH, "//android.view.View[contains(@text, '{}') and @index='2']".format(var))
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststep
    def wechat_back_up_btn(self):
        """微信退回按钮"""
        locator = (By.ID, self.id_type() + 'dn')
        return self.get_wait_check_page_ele(locator, applets=False)

    @teststeps
    def readd_applet_operate(self):
        """删除小程序重新添加过程"""
        applet_name = "百项过智能学习中心"
        self.discovery_tab().click()
        applet_title = self.wait_check_find_page()
        if applet_title:
            applet_title.click()
            # 删除小程序
            if self.wait_check_applet_list_page():
                test_applet = self.wait_check_test_applet(applet_name)
                if test_applet:
                    TouchAction(self.driver).long_press(test_applet).perform()
                    self.delete_applet().click()
            # 重新添加小程序
            self.wechat_back_up_btn().click()
            if self.wait_check_find_page():
                self.find_icon().click()
                if self.wait_check_search_page():
                    self.search_input_ele().send_keys(applet_name)
                    self.search_applet().click()
                if self.wait_check_search_applet_result_page(applet_name):
                    self.find_test_applet(applet_name).click()





