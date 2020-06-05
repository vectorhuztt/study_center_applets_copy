from math import ceil

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.books.books_page import BooksPage
from app.passion_applets.object_page.applets.books.unit_page import UnitPage
from app.passion_applets.object_page.applets.home.home_page import AppletsHomePage
from app.passion_applets.object_page.sql.sql_handler import SqlHandler
from conf.base_page import BasePage
from conf.decorator import teststep
from utils.date_valid import ValidDate


class BookDataValidatePage(BasePage):
    def __init__(self):
        self.home = AppletsHomePage()
        self.sql_handler = SqlHandler()

    @teststep
    def current_unit(self):
        """当前单元"""
        locator = (By.CSS_SELECTOR, 'wx-circle-progress-bar:nth-child(1) .CircleProgressBar-index--value')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def total_unit(self):
        """单元总数"""
        locator = (By.CSS_SELECTOR, 'wx-circle-progress-bar:nth-child(1) .CircleProgressBar-index--total')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def unit_studied_word_count(self):
        """单元已学单词数"""
        locator = (By.CSS_SELECTOR, 'wx-circle-progress-bar:nth-child(2) .CircleProgressBar-index--value')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def unit_words_total_count(self):
        """单元单词总数"""
        locator = (By.CSS_SELECTOR, 'wx-circle-progress-bar:nth-child(2) .CircleProgressBar-index--total')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def book_total_studied_count(self):
        """累计学习单词个数"""
        locator = (By.CSS_SELECTOR, 'wx-circle-progress-bar:nth-child(3) .CircleProgressBar-index--value')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def book_total_words_count(self):
        """书籍全部单词个数"""
        locator = (By.CSS_SELECTOR, 'wx-circle-progress-bar:nth-child(3) .CircleProgressBar-index--total')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def get_level_words(self, total_words):
        """获取每一关卡对应的单词数"""
        unit_word_list = []
        total_level_count = ceil(total_words / 10)
        for x in range(total_level_count):
            if x == total_level_count - 1:
                unit_word_list.append(total_words % 10)
            else:
                unit_word_list.append(10)
        return unit_word_list

    @teststep
    def check_book_total_count(self, book_id, is_login):
        """
            书籍总数校对
            :param 书籍id
            :returns  book_label_id 书籍对应的标签id
                      book_unit_ids 书籍下所有单元id
                      book_total_word_count 书籍对应的单词个数
        """
        book_label_id = self.sql_handler.get_book_related_label_id(book_id)
        book_unit_ids = self.sql_handler.get_book_unit_ids(book_label_id)
        book_total_word_count = self.sql_handler.get_book_word_count(book_unit_ids)
        if not is_login:
            total_count = 50 if book_total_word_count >= 50 else book_total_word_count
        else:
            total_count = book_total_word_count
        print('书本对应的标签id:', book_label_id)

        # 校验页面书籍总数个数
        page_book_total_count = ValidDate.get_single_num_from_text(self.book_total_words_count().text)
        print('查询书籍单词总数为：', total_count)
        print('页面书籍单词总数为：', page_book_total_count, '\n')
        if int(total_count) != page_book_total_count:
            self.base_assert.except_error('数据库查询的书籍单词总数与页面不一致， 查询得{}, 页面为{}'
                                          .format(total_count, page_book_total_count))
        return book_label_id, book_unit_ids, total_count

    @teststep
    def check_unit_count(self, book_total_word_count, book_unit_ids, is_login):
        """
            单元或者关卡数校对
            :param book_total_word_count 书籍总单词数
            :param book_unit_ids 书籍各单元的id
            :param is_login 是否已绑定账号
        """
        page_unit_count = ValidDate.get_single_num_from_text(self.total_unit().text)
        check_unit_count = len(book_unit_ids) if is_login else ceil(book_total_word_count / 10)
        print('查询书籍单元数为：', check_unit_count)
        print('页面书籍单元数为：', page_unit_count, '\n')
        if check_unit_count != page_unit_count:
            self.base_assert.except_error('数据库查询的单元总数与页面不一致， 查询得{}, 页面为{}'
                                          .format(check_unit_count, page_unit_count))

    @teststep
    def check_unit_total_count(self, book_total_word_count, book_unit_ids, is_login):
        """
            单元/关卡单词总数校验
            :param book_total_word_count 书籍总单词数
            :param book_unit_ids 书籍各单元的id
            :param is_login 是否已绑定账号
            :return current_unit_id 当前单元id
        """
        current_unit_id = 0
        current_unit_index = int(self.current_unit().text)
        page_unit_total_count = ValidDate.get_single_num_from_text(self.unit_words_total_count().text)
        if is_login:
            current_unit_id = book_unit_ids[current_unit_index - 1]
            current_unit_total_count = self.sql_handler.get_unit_word_count(current_unit_id)
        else:
            unit_word_list = self.get_level_words(book_total_word_count)
            current_unit_total_count = unit_word_list[current_unit_index - 1]
        print('当前单元单词总数：', page_unit_total_count)
        print('当前单元数据查询单词总数：', current_unit_total_count, '\n')
        if current_unit_total_count != page_unit_total_count:
            self.base_assert.except_error('数据库查询的单元/关卡单词总数与页面不一致， 查询得{}, 页面为{}'
                                          .format(page_unit_total_count, current_unit_total_count))
        return current_unit_id

    @teststep
    def check_unit_studied_count(self, student_id, current_unit_id, is_login):
        """
            单元/关卡已学数据校验
            :param  student_id 学生id
            :param current_unit_id 当前单元id
            :param is_login 是否已登录
        """
        page_unit_studied_count = ValidDate.get_single_num_from_text(self.unit_studied_word_count().text)
        if is_login:
            current_unit_studied_count = self.sql_handler.get_unit_studied_count(student_id, current_unit_id)
        else:
            current_unit_studied_count = self.sql_handler.get_unit_studied_count(student_id, current_unit_id, is_login)
        print('当前单元已学单词总数：', page_unit_studied_count)
        print('当前单元查询已学单词总数：', current_unit_studied_count, '\n')
        if current_unit_studied_count != page_unit_studied_count:
            self.base_assert.except_error('数据库查询的单元/关卡单词已学数与页面不一致， 查询得{}, 页面为{}'
                                          .format(current_unit_studied_count, page_unit_studied_count))

    @teststep
    def check_book_studied_count(self, student_id, book_label_id, book_unit_ids, is_login):
        """书籍总共学习单词数校验"""
        page_book_studied_count = ValidDate.get_single_num_from_text(self.book_total_studied_count().text)
        if is_login:
            current_book_studied_count = sum(
                [self.sql_handler.get_unit_studied_count(student_id, x) for x in book_unit_ids])
        else:
            current_book_studied_count = self.sql_handler.get_unit_studied_count(student_id, book_label_id, is_login)
        print('当前书籍已学单词总数：', page_book_studied_count)
        print('当前书籍查询已学单词总数：', current_book_studied_count, '\n')
        if current_book_studied_count != page_book_studied_count:
            self.base_assert.except_error('数据库查询的当前书籍已学单词数与页面不一致， 查询得{}, 页面为{}'
                                          .format(current_book_studied_count, page_book_studied_count))
        return page_book_studied_count

    @teststep
    def check_book_data(self, student_id, book_info, is_login):
        """书籍数据校验"""
        book_name = book_info['book_name']
        book_id = book_info['book_id']
        print('书籍id：', book_id)
        if self.home.wait_check_applets_home_page():
            current_book_name = self.home.current_book_name().text
            if not book_name:
                print('未选择任何书籍')
            else:
                if current_book_name != book_name:
                    self.base_assert.except_error("选择的书籍名称与页面显示的名称不一致")

        # 校验书籍总数
        book_label_id, book_unit_ids, book_total_word_count = self.check_book_total_count(book_id, is_login)
        # 校验单元数
        self.check_unit_count(book_total_word_count, book_unit_ids, is_login)
        # 校验当前单元单词总数
        current_unit_id = self.check_unit_total_count(book_total_word_count, book_unit_ids, is_login)
        # 校验当前单元已学数
        self.check_unit_studied_count(student_id, current_unit_id, is_login)
        # 校验当前书籍已学总数
        book_studied_count = self.check_book_studied_count(student_id, book_label_id, book_unit_ids, is_login)

        return book_studied_count

    @teststep
    def select_one_book_and_check_data(self, user_id, first_index=None, second_index=None, book_index=None):
        """
            选择一本书籍操作
            :param user_id 学生id
            :param first_index 一级标签索引
            :param second_index 二级标签索引
            :param book_index 书籍标签索引
        """
        if self.home.wait_check_applets_home_page():
            self.home.current_book_name().click()
            # 随机选择一本书
            book_info = BooksPage().select_label_books_operate(first_index, second_index, book_index)
            # 校验页面数据
            book_studied_count = BookDataValidatePage().check_book_data(user_id, book_info, is_login=True)
            book_info['studied_count'] = book_studied_count
            self.home.start_game_btn().click()
            unit_index = UnitPage().select_unit_operate(book_info['book_name'], book_studied_count)
            book_info['unit_index'] = unit_index
            return book_info
