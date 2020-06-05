import random

from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator import teststep


class UnitPage(BasePage):

    @teststep
    def wait_check_select_unit_page(self):
        """选择单元页面检查点"""
        locator = (By.CSS_SELECTOR, '.subtitle')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_empty_page(self):
        """暂无复习数据页面检查点"""
        locator = (By.CSS_SELECTOR, '.empty')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def current_book(self):
        """当前课程名称"""
        locator = (By.CSS_SELECTOR, '.highlighted')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def unit_list(self):
        """单元列表"""
        locator = (By.CSS_SELECTOR, '.unit-list .item')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def unit_back_btn(self):
        """选择单元回退页面"""
        locator = (By.CSS_SELECTOR, '.NavigationBar-index--back')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def select_unit_operate(self, book_name, book_studied_count):
        """选择单元操作"""
        if not self.wait_check_select_unit_page():
            self.base_assert.except_error('未进入选择单元页面')
        else:
            if self.current_book().text != book_name:
                self.base_assert.except_error("页面的课程名称与已选择的书籍名称不一致")
            if book_studied_count:
                if self.wait_check_empty_page():
                    self.base_assert.except_error('书籍存在已学习单词， 但是选择单元页面无单元可选')

            if not book_studied_count:
                if not self.wait_check_empty_page():
                    self.base_assert.except_error('书籍不存在已学单词， 但是选择单元页面存在可选择单元')

            unit_list = self.unit_list()
            if unit_list:
                range_num = len(unit_list) if len(unit_list) < 8 else 8
                random_index = random.choice(range(range_num))
                unit_list[random_index].click()
                return random_index
            return False
