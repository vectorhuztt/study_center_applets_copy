import random
import time

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.common import CommonPage
from conf.decorator import teststep, teststeps


class WordChoiceGame(CommonPage):

    @teststep
    def wait_check_word_choice_page(self):
        """词汇选择页面检查点"""
        locator = (By.CSS_SELECTOR, '.CHXZ-index--option')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def hidden_right_word_explain(self):
        """单词隐藏解释页面检查点"""
        locator = (By.CSS_SELECTOR, '.CHXZ-index--explain.CHXZ-index--hidden')
        return self.get_wait_check_page_ele(locator, timeout=3)

    @teststep
    def hidden_right_word(self):
        """单词隐藏单词页面检查点"""
        locator = (By.CSS_SELECTOR, '.CHXZ-index--word.CHXZ-index--hidden')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_right_opt_page(self):
        """正确选项页面检查点"""
        locator = (By.CSS_SELECTOR, '.CHXZ-index--success')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def choice_voice_btn(self):
        """词汇选择喇叭按钮"""
        locator = (By.CSS_SELECTOR, '.CHXZ-index--quiz-voice')
        return self.get_wait_check_page_ele(locator, timeout=5)

    @teststep
    def choice_options(self):
        """词汇选择选项"""
        locator = (By.CSS_SELECTOR, '.CHXZ-index--option')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def word_choice_next_btn(self):
        """词汇选择页面检查点"""
        locator = (By.CSS_SELECTOR, '.CHXZ-index--quiz-button')
        return self.get_wait_check_page_ele(locator, timeout=5)

    @teststep
    def word_choice_do_process(self, right_answer, do_right=False):
        for opt in self.choice_options():
            if do_right:
                if opt.text == right_answer:
                    print('选择单词：', opt.text)
                    opt.click()
                    time.sleep(3)
                    break
            else:
                if opt.text != right_answer:
                    print('选择单词：', opt.text)
                    opt.click()
                    time.sleep(1)
                    break

    @teststeps
    def word_choice_game_operate(self, mode, word_info: dict, *, do_right: bool, bank_index: list,
                                 wrong_index: list, right_info: list, record_id_info: dict,
                                 type_list: list, word_count: int, is_review: bool):
        """
            词汇选择做题过程
            :param mode 词汇选择类型
            :param word_info 正确单词信息
            :param do_right  是否做对
            :param bank_index 全局的题目索引
            :param wrong_index 词汇选择的错题索引
            :param right_info  词汇选择各类型对应的做对单词
            :param record_id_info 记录单词id
            :param type_list 记录游戏类型
            :param word_count 单词个数
            :param is_review 是否是复习状态

        """
        print('--- 听音选词 ---\n') if mode == 'TX' else print('--- 汉译英 ---\n')

        while self.wait_check_word_choice_page():
            # 判断词汇选择类型是否发生变化, 变化则退出，在外层更换index_info
            game_mode = 'TX' if self.hidden_right_word_explain() else "HY"
            if mode != game_mode:
                break
            # 判断下一题按钮是否出现
            if self.word_choice_next_btn():
                self.base_assert.except_error('未答题已显示下一题按钮')

            bank_id = self.game_id()
            wrong_bank_id = list(word_info.keys())[0]
            print('解释id：', bank_id)
            print('错题id：', wrong_bank_id)

            # 判断当前计数是否与出现的id一致
            game_type = self.exclude_flask_index_judge(type_list, record_id_info, word_info, word_count, is_review)

            # 判断单词做对之后是否再次出现
            if bank_id in right_info:
                self.base_assert.except_error('单词已做对， 但是再次出现 ' + bank_id)

            if game_mode == 'TX':
                self.choice_voice_btn().click()
                time.sleep(1)

            right_answer = word_info[bank_id]['word']
            print('正确答案：', right_answer)

            if do_right:
                self.word_choice_do_process(right_answer=right_answer, do_right=True)
                right_info.append(bank_id)
            else:
                if bank_id != wrong_bank_id:
                    self.word_choice_do_process(right_answer=right_answer, do_right=True)
                    right_info.append(bank_id)
                else:
                    wrong_index.append(bank_index[0])
                    wrong_count = len(wrong_index)
                    print('此单词错误次数：', wrong_count)
                    if wrong_count >= 5:
                        right_info.append(bank_id)
                    self.word_choice_do_process(right_answer=right_answer)

                    if not self.wait_check_right_opt_page():
                        self.base_assert.except_error('已选择错误选项，未显示正确选项')
                    if game_mode == 'TX':
                        if self.hidden_right_word_explain():
                            self.base_assert.except_error('已点击错误选项， 未显示出解释文本')

                    if game_mode == 'HY':
                        if not self.choice_voice_btn():
                            self.base_assert.except_error('汉译英游戏完毕后未出现喇叭按钮')

                        if self.hidden_right_word():
                            self.base_assert.except_error('已点击错误选项， 未显示出正确单词文本')
                    self.next_btn_operate(self.word_choice_next_btn)
            if bank_id not in record_id_info[game_type]:
                record_id_info[game_type].append(bank_id)
            bank_index[0] += 1
            print(wrong_index)
            print('-'*30, '\n')







