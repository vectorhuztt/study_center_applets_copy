import time


class AppletUtil:
    @classmethod
    def switch_to_context(cls, driver, context='NATIVE'):
        """
        切换上下文，这里可能有多个，需要匹配，例如 NATIVE_APP、WEBVIEW_com.tencent.mm:tools、WEBVIEW_com.tencent.mm:appbrand0
        """
        contexts = driver.contexts
        for cnt in contexts:
            if context in cnt:
                driver.switch_to.context(cnt)
                return True
        return False

    @classmethod
    def switch_to_active_applet_window(cls, driver):
        """
        一个 webview 会有多个窗口对象（每个窗口对应一个小程序页面），切换到当前激活的窗口。需要在 WEBVIEW 环境执行
        """
        windows = driver.window_handles

        for window in windows:
            driver.switch_to.window(window)
            if ':VISIBLE' in driver.title:
                return True
        return False

    @classmethod
    def scroll_webview_screens(cls, driver, pages=1, direction='down'):
        """
        向下滑动指定的页数，每次滑动一个可见的滑动区域范围。需要在 WEBVIEW 环境执行
        :param driver:
        :param pages: 滑动页面数量
        :param direction: 滑动方向，默认往下滑动
        """
        for i in range(0, pages):
            # TODO 这个滑动的距离需要结合手机调试确定
            if direction == 'down':
                driver.execute_script("window.scrollBy(0, window.screen.availHeight - 170)")
            elif direction == 'up':
                driver.execute_script("window.scrollBy(0, 170 - window.screen.availHeight)")
            time.sleep(0.5)

    @classmethod
    def window_status_judge(cls, driver):
        current_title = driver.title
        if ':INVISIBLE' in current_title:
            cls.switch_to_active_applet_window(driver)
            time.sleep(2)

    @classmethod
    def switch_operate(cls, driver, switch_to_app=False):
        if switch_to_app:
            cls.switch_to_context(driver)
        else:
            cls.switch_to_context(driver, context='com.tencent.mm:appbrand0')
            cls.switch_to_active_applet_window(driver)
        time.sleep(3)
