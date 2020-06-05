import random
import time

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.common import CommonPage
from conf.decorator import teststep, teststeps


class BooksPage(CommonPage):
    @teststep
    def wait_check_books_page(self):
        """选书页面检查点"""
        locator = (By.CSS_SELECTOR, '.subject-list')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def subject_first_label(self):
        """课程一级标签"""
        locator = (By.CSS_SELECTOR, '.subject-list .subject')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def subject_second_label(self):
        """课程二级标签"""
        locator = (By.CSS_SELECTOR, '.label-list-wrapper .label')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def label_books_view(self):
        """标签下书籍图片"""
        locator = (By.CSS_SELECTOR, '.course-wrapper .course')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def label_books_names(self):
        """标签下书籍名称"""
        locator = (By.CSS_SELECTOR, '.course-wrapper .course .course-name')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def get_random_index(self, length, start=0):
        """获取"""
        limit_length = length if length <= 6 else 6
        return random.choice(range(start, limit_length))

    @teststeps
    def select_label_books_operate(self, first_index=None, second_index=None, book_index=None):
        """选书操作"""
        if self.wait_check_books_page():
            print('<=== 选择书籍页面 ===>\n')
            first_labels = self.subject_first_label()
            if not first_labels:
                self.base_assert.except_error('未发现页面的一级标签')
                return {}
            first_select_index = first_index - 1 if first_index else self.get_random_index(len(first_labels))
            first_labels[first_select_index].click()
            time.sleep(1)
            second_labels = self.subject_second_label()
            if not second_labels:
                self.base_assert.except_error('该标签下暂无二级标签')
                return {}

            second_select_index = second_index - 1 if second_index else self.get_random_index(len(second_labels), start=1)
            second_labels[second_select_index].click()
            time.sleep(2)
            books = self.label_books_names()
            if not books:
                self.base_assert.except_error('该标签下暂`   无书籍')
            else:
                book_select_index = book_index - 1 if book_index else self.get_random_index(len(books))
                book_name = books[book_select_index].text
                print('选择书籍：', book_name)
                book_view = self.label_books_view()[book_select_index]
                book_id = book_view.get_attribute('data-id')
                book_view.click()
                time.sleep(5)
                self.applet_util.switch_to_active_applet_window(self.driver)
                return {'book_id': book_id, "book_name": book_name}


