from selenium.webdriver.common.by import By
from app.passion_applets.object_page.applets.common import CommonPage

from conf.decorator import teststep, teststeps


class AppletsHomePage(CommonPage):

    @teststep
    def wait_check_applets_home_page(self):
        """小程序主页"""
        locator = (By.CLASS_NAME, 'main')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_start_tip_image(self):
        """开始闯关提示"""
        locator = (By.CSS_SELECTOR, '.main-tip-image')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_course_tip_image(self):
        """开始闯关提示"""
        locator = (By.CSS_SELECTOR, '.tip-image')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_add_applet_desktop(self):
        """添加快捷方式"""
        locator = (By.CSS_SELECTOR, '.Favorite-index--close')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_permit_tip(self):
        """授权文本提示"""
        locator = (By.CSS_SELECTOR, '.user-info wx-button[open-type]')
        return self.get_wait_check_page_ele(locator)

    # 下方tab按钮
    @teststep
    def rank_tab(self):
        """排行"""
        locator = (By.CSS_SELECTOR, ".tab-bar .item:nth-child(1)")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def summary_tab(self):
        """汇总"""
        locator = (By.CSS_SELECTOR, ".tab-bar .item:nth-child(2)")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def mine_tab(self):
        """我的"""
        locator = (By.CSS_SELECTOR, '.tab-bar .item:nth-child(3)')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def today_study_count(self):
        """今日学习任务"""
        locator = (By.CSS_SELECTOR, '.wrapper  .bottom wx-text')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def current_book_name(self):
        """当前图书名称"""
        locator = (By.CSS_SELECTOR, '.course-name')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def start_game_btn(self):
        """开始闯关按钮"""
        locator = (By.CSS_SELECTOR, '.button-wrapper  .van-button')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def activity_status(self):
        activity = self.wait_activity()
        if activity == '':  # 崩溃退出
            self.applet_util.switch_operate(self.driver, switch_to_app=True)
            self.driver.launch_app()  # 重启APP
            self.wechat.enter_into_applet_operate()
            if self.wait_check_applets_home_page():  # 在主界面
                print('主界面')
        else:
            if self.wechat.wait_check_wechat_home_page():
                self.wechat.enter_into_applet_operate()
            else:
                if not self.wait_check_applets_home_page():  # 在主界面
                    self.applet_util.switch_operate(self.driver, switch_to_app=True)
                    self.driver.close_app()  # 关闭APP
                    self.driver.launch_app()  # 重启APP
                    self.wechat.enter_into_applet_operate()

