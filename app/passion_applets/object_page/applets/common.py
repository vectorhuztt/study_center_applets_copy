import time

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.sql.sql_handler import SqlHandler
from app.passion_applets.object_page.wechat.wechat_page import WeChatPage
from conf.base_page import BasePage
from conf.decorator import teststep
from utils.wxapp import AppletUtil


class CommonPage(BasePage):
    def __init__(self):
        self.wechat = WeChatPage()
        self.applet_util = AppletUtil
        self.sql_handler = SqlHandler()

    def applet_back_btn(self):
        """小程序退回按钮"""
        locator = (By.CSS_SELECTOR, '.back')
        return self.get_wait_check_page_ele(locator, timeout=5)

    def applet_index_back_btn(self):
        locator = (By.CSS_SELECTOR, '.index--back')
        return self.get_wait_check_page_ele(locator, timeout=5)

    @teststep
    def click_applet_back_btn(self):
        """点击退回按钮操作"""
        try:
            self.applet_back_btn().click()
        except:
            self.applet_index_back_btn().click()
        time.sleep(5)
        self.applet_util.switch_to_active_applet_window(self.driver)

    @teststep
    def current_index(self):
        """当前index"""
        locator = (By.CSS_SELECTOR, ".ProgressLayout-index--info")
        ele = self.get_wait_check_page_ele(locator, timeout=5)
        return int(ele.text.split('/')[0])

    @teststep
    def bank_count(self):
        """总题数"""
        locator = (By.CSS_SELECTOR, ".ProgressLayout-index--total")
        ele = self.get_wait_check_page_ele(locator)
        return int(ele.text.split('/')[1])

    @teststep
    def game_container(self):
        """游戏容器"""
        locator = (By.CSS_SELECTOR, '.ProgressLayout-index--progress-layout-wrapper [class*="index--container"]')
        container_ele = self.get_wait_check_page_ele(locator)
        return container_ele.get_attribute('class')

    @teststep
    def game_id(self):
        """单词id"""
        locator = (By.CSS_SELECTOR, '.BasicLayout-index--basic-layout-wrapper wx-view[data-code]')
        ele = self.get_wait_check_page_ele(locator)
        word_id = ele.get_attribute('data-id')
        return word_id

    @teststep
    def current_index_judge(self, index):
        """当前索引校对"""
        current_index = self.current_index()
        if current_index != index:
            self.base_assert.except_error('当前题目索引与做题个数不一致， 页面索引为%d, '
                                          '实际应为%d' % (current_index, index))

    @teststep
    def exclude_flask_index_judge(self, type_list, record_id_info, all_word_info,
                                  word_count, is_review=False):
        """
            出去闪卡的当前索引判断
            :param type_list: 题目类型列表
            :param record_id_info 记录的id信息
            :param all_word_info 所有单词信息
            :param word_count 单词个数
            :param is_review 当前是否是复习状态
        """
        try:
            game_type = type_list[-2]
            if len(record_id_info[game_type]) >= len(all_word_info):
                game_type = type_list[-1]
            if game_type == '还原单词':
                if len(record_id_info[game_type]) >= word_count:
                    game_type = type_list[-1]
        except:
            game_type = type_list[-1]
        record_ids = record_id_info[game_type]
        if game_type == '还原单词' and is_review:
            final_length = len(record_ids) - 1 if len(record_ids) + 1 > len(all_word_info) else len(record_ids)
        else:
            final_length = 0 if len(record_ids) + 1 > len(all_word_info) else len(record_ids)
        self.current_index_judge(final_length + 1)
        return game_type

    @teststep
    def btn_status_judge(self, func, flag=False):
        """按钮状态判断"""
        ele = func()
        ele_class = ele.get_attribute('class')
        if flag:
            if 'disabled' in ele_class:
                self.base_assert.except_error('按钮状态应为激活状态，此时为置灰状态')
        else:
            if 'disabled' not in ele_class:
                self.base_assert.except_error('按钮状态应为置灰状态， 此时为激活状态')

    @teststep
    def next_btn_isvisible_judge(self, func, is_visible=False):
        ele = func()
        if is_visible:
            if not ele:
                self.base_assert.except_error('未发现下一步按钮')
        else:
            if ele:
                self.base_assert.except_error('未做题下一步按钮默认出现')

    @teststep
    def next_btn_operate(self, func):
        """下一步按钮处理方法"""
        ele = func()
        if not ele:
            self.base_assert.except_error('已完成题目，页面未出现下一步按钮')
        else:
            ele_class = ele.get_attribute('class')
            if 'disabled' in ele_class:
                self.base_assert.except_error('按钮状态应为激活状态， 此时为置灰状态')
            else:
                ele.click()
                time.sleep(2)