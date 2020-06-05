import time

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.common import CommonPage
from conf.decorator import teststep


class ReformWordGame(CommonPage):
    @teststep
    def wait_check_reform_word_page(self):
        """还原单词页面检查点"""
        locator = (By.CSS_SELECTOR, '.HYDC-index--container')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_clear_btn_page(self):
        """清除按钮页面检查点"""
        locator = (By.CSS_SELECTOR, '.HYDC-index--clear.HYDC-index--hide')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def word_explain(self):
        """单词解释"""
        locator = (By.CSS_SELECTOR, '.HYDC-index--explain')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def word_alphas(self):
        """拆分字母"""
        locator = (By.CSS_SELECTOR, '.HYDC-index--letter')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def clear_btn(self):
        """清除按钮"""
        locator = (By.CSS_SELECTOR, '.HYDC-index--clear')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def submit_btn(self):
        """提交按钮"""
        locator = (By.CSS_SELECTOR, '.HYDC-index--quiz-button')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def finish_word(self):
        """完成单词"""
        locator = (By.CSS_SELECTOR, '.HYDC-index--answer')
        ele = self.get_wait_check_page_ele(locator, single=False)
        words = [x.text for x in ele]
        return ''.join(words)

    @teststep
    def reform_do_right_operate(self, answer_word, submit=True):
        """还原单词正确操作"""
        index = 0
        while answer_word.strip() != self.finish_word():
            wait_select_words = self.word_alphas()
            for x in range(len(wait_select_words)):
                wait_alpha = wait_select_words[x].text.strip()
                alpha_length = len(wait_alpha)
                if index + alpha_length >= len(answer_word) - 1:
                    answer_word += ' ' * alpha_length
                word_part = answer_word[index:index + alpha_length].strip()
                if wait_alpha and wait_alpha == word_part:
                    wait_select_words[x].click()
                    time.sleep(0.5)
                    index += alpha_length
                    break
        if submit:
            print('还原后的单词：', self.finish_word())
            self.next_btn_operate(self.submit_btn)
            time.sleep(4)

    @teststep
    def reform_do_wrong_operate(self, answer_word, submit=True):
        """还原单词错误操作"""
        wait_select_words = self.word_alphas()
        count = 0
        for x in range(len(wait_select_words)):
            alpha_length = len(wait_select_words[x].text.strip())
            word_part = answer_word[:alpha_length]
            if count == 0:
                if wait_select_words[x].text.strip() != word_part.strip():
                    wait_select_words[x].click()
                    break

        while self.word_alphas():
            self.word_alphas()[0].click()
            time.sleep(0.5)

        if submit:
            print('还原后的单词：', self.finish_word())
            self.next_btn_operate(self.submit_btn)
            self.submit_btn().click()
            time.sleep(4)

    @teststep
    def reform_word_game_operate(self, word_info: dict, *, do_right: bool, bank_index: list,
                                 wrong_index: list, right_info: list, record_id_info: dict,
                                 type_list: list, word_count: int, is_review: bool):
        """
            还原单词游戏过程
            :param word_info 正确单词信息(仅有单词)
            :param do_right 是否做对
            :param bank_index 全局题目索引
            :param wrong_index 错误单词/短语索引
            :param right_info 正确单词/短语信息
            :param record_id_info 记录的单词/短语id
            :param type_list 记录的游戏类型
            :param word_count 记录单词的个数
            :param is_review 是否是复习状态
        """
        print('---- 还原单词 -----\n')
        while self.wait_check_reform_word_page():
            is_submit = True  # 记录此次做题是否点击了提交按钮
            bank_id = self.game_id()
            self.btn_status_judge(self.submit_btn)
            print('单词id：', bank_id)
            # 判断单词做对， 是否再次出现
            if bank_id in right_info:
                self.base_assert.except_error('单词已做对， 但是再次出现 ' + bank_id)
            # 判断当前计数是否与出现的id一致
            game_type = self.exclude_flask_index_judge(type_list, record_id_info, word_info, word_count, is_review)

            word_explain = self.word_explain().text
            right_answer = word_info[bank_id]['word']
            wrong_bank_id = list(word_info.keys())[0]
            print('错题id：', wrong_bank_id)
            print('单词解释：', word_explain)
            print('正确答案：', right_answer)
            print('还原前单词：', [x.text for x in self.word_alphas()])

            if do_right:
                self.reform_do_right_operate(right_answer)
                right_info.append(bank_id)
            else:
                if bank_id != wrong_bank_id:
                    if len(right_info) == 1:
                        self.reform_do_wrong_operate(right_answer, submit=False)
                        if self.wait_check_clear_btn_page():
                            self.base_assert.except_error('点击分割字母后， 未出现清除按钮')
                        else:
                            self.clear_btn().click()
                            time.sleep(1)
                            if self.finish_word():
                                self.base_assert.except_error('★★★ 点击清除按钮后，已选选项未清空')
                    right_info.append(bank_id)
                    self.reform_do_right_operate(right_answer)
                else:
                    wrong_index.append(bank_index[0])
                    wrong_count = len(wrong_index)
                    print('此单词错误次数：', wrong_count)
                    if wrong_count >= 5:
                        right_info.append(bank_id)
                    self.reform_do_wrong_operate(right_answer)
            if is_submit:
                if bank_id not in record_id_info[game_type]:
                    record_id_info[game_type].append(bank_id)
                bank_index[0] += 1
                print(wrong_index)
                print('-' * 30, '\n')

