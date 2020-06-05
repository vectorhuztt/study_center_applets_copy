import random
import string
import time

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.common import CommonPage
from app.passion_applets.object_page.applets.games.word_reform import ReformWordGame
from conf.decorator import teststep


class WordSpellGame(CommonPage):

    def __init__(self):
        super().__init__()
        self.word_reform = ReformWordGame()

    @teststep
    def wait_check_spell_page(self):
        """单词拼写页面检查点"""
        locator = (By.CSS_SELECTOR, '.DCPX-index--container')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_random_spell_page(self):
        """单词随机拼写页面检查点"""
        locator = (By.CSS_SELECTOR, '.DCPX-index--input.DCPX-index--spell')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_spell_right_word_page(self):
        """随机拼写正确单词页面检查点"""
        locator = (By.CSS_SELECTOR, '.DCPX-index--word.DCPX-index--visible')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_listen_spell_page(self):
        """单词听写页面检查点"""
        locator = (By.CSS_SELECTOR, '.DCPX-index--quiz-voice')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def word_explain(self):
        """单词解释"""
        locator = (By.CSS_SELECTOR, '.DCPX-index--explain')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def word_input_wrap(self):
        """拼写输入栏"""
        locator = (By.CSS_SELECTOR, '.DCPX-index--input')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def random_input_warp(self):
        """随机拼写输入栏"""
        locator = (By.CSS_SELECTOR, '.DCPX-index--blank')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def forget_btn(self):
        """忘记了按钮"""
        locator = (By.XPATH, "//wx-view[@class='DCPX-index--container']//span[2][contains(text(),'忘记了')]/..")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def keyboard_key(self, word_alpha):
        """键盘字母定位"""
        locator = (By.XPATH, '//wx-view[@class="Keyboard-index--letter-wrap"]//'
                             'span[2][text()="{}"]'.format(word_alpha))
        return self.get_wait_check_page_ele(locator)

    @teststep
    def keyboard_icon_key(self):
        """键盘图标键"""
        locator = (By.CSS_SELECTOR, '.Keyboard-index--icon')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def enter_key(self):
        """键盘字母定位"""
        locator = (By.CSS_SELECTOR, '.Keyboard-index--letter-wrap')
        ele = self.get_wait_check_page_ele(locator, single=False)
        return ele[-1]

    @teststep
    def page_alpha(self):
        """获取挖空后的单词"""
        locator = (By.CSS_SELECTOR, '.DCPX-index--spell wx-text')
        ele = self.get_wait_check_page_ele(locator, single=False)
        alpha_list = []
        for x in ele:
            if x.text == '':
                alpha_list.append('_')
            else:
                alpha_list.append(x.text)
        return alpha_list

    @teststep
    def input_word_operate(self, input_words, do_right):
        for alpha in input_words:
            if alpha == ' ':
                continue
            self.keyboard_key(alpha).click()
        self.enter_key().click()
        if not do_right:
            if not self.wait_check_spell_right_word_page():
                self.base_assert.except_error('提交拼写后，未发现随机拼写的正确单词')
            self.enter_key().click()
            time.sleep(2)
        else:
            time.sleep(4)

    @teststep
    def random_spell_operate(self, right_answer, do_right):
        """随机拼写操作"""
        if self.wait_check_random_spell_page():
            print('---- 随机拼写游戏 ----\n')
            page_word = self.page_alpha()
            input_list = [y for x, y in zip(page_word, right_answer) if x != y]
            random_str = random.sample(string.ascii_lowercase, len(input_list))
            input_alphas = input_list if do_right else random_str
            print('输入单词：', input_alphas, '\n')
            self.input_word_operate(input_alphas, do_right=do_right)

    @teststep
    def spell_operate(self, right_answer, wrong_count=None, do_right=False, is_review=False):
        """拼写单词操作"""
        if do_right:
            input_word = right_answer
        else:
            length = random.choice(range(2, 5))
            input_word = random.sample(string.ascii_lowercase, length)
        print('输入单词：', input_word, '\n')
        self.input_word_operate(input_word, do_right=do_right)

        #  插入错题游戏  随机拼写、还原单词
        if not do_right and not is_review:
            if wrong_count < 5:
                status = random.choice([True, False])
                if not self.wait_check_random_spell_page():
                    self.base_assert.except_error('单词拼写错误后， 未进入随机拼写页面')
                else:
                    self.random_spell_operate(right_answer, do_right=status)
            else:
                if self.wait_check_random_spell_page():
                    self.base_assert.except_error('单词拼写错误第五次依然会有随机拼写游戏')

    @teststep
    def spell_word_game_operate(self, all_word_info: dict, *, do_right: bool, bank_index: list, wrong_index: list,
                                right_info: list, skip_index_info: list, record_id_info: dict,
                                type_list: list, word_count: int, is_review: bool):
        """
            单词拼写页面
            :param all_word_info 正确单词/短语信息
            :param do_right  是否做对
            :param bank_index 全局的题目索引
            :param wrong_index 单词拼写的错题索引
            :param right_info  单词拼写的的做对单词
            :param skip_index_info  跳过的索引信息
            :param record_id_info 记录的单词/短语id
            :param type_list 记录的游戏类型
            :param word_count 单词个数
            :param is_review 是否是复习状态
        """
        while self.wait_check_spell_page():
            bank_id = self.game_id()
            # 判断做对单词是否再次出现
            if bank_id in right_info:
                self.base_assert.except_error('单词已完成， 但是再次出现 ' + bank_id)

            # 判断当前计数是否与出现的id一致
            game_type = self.exclude_flask_index_judge(type_list, record_id_info, all_word_info, word_count, is_review)

            right_answer = all_word_info[bank_id]['word']
            wrong_bank_id = list(all_word_info.keys())[0]
            print('单词id：', bank_id)
            print('单词解释：', self.word_explain().text)
            print('正确答案：', right_answer)
            skip_id = list(all_word_info.keys())[1] if len(all_word_info) > 1 else -1

            if do_right:
                self.spell_operate(right_answer, do_right=True, is_review=is_review)
                right_info.append(bank_id)
            else:
                if wrong_bank_id == bank_id:
                    wrong_index.append(bank_index[0])
                    bank_count = len(wrong_index)
                    if bank_count >= 5:
                        right_info.append(bank_id)
                    if is_review:
                        self.spell_operate(right_answer, is_review=True)
                    else:
                        self.spell_operate(right_answer, wrong_count=len(wrong_index))

                else:
                    if is_review:
                        right_info.append(bank_id)
                        self.spell_operate(right_answer, do_right=True)
                    else:
                        if bank_id != skip_id:
                            right_info.append(bank_id)
                            self.spell_operate(right_answer, do_right=True)
                        else:
                            self.forget_btn().click()
                            skip_index_info.append(bank_index[0])
                            if len(skip_index_info) >= 5:
                                right_info.append(bank_id)
                                if self.wait_check_listen_spell_page():
                                    self.base_assert.except_error('跳过第五次依然会出现听写游戏')
                            else:
                                if not self.wait_check_listen_spell_page():
                                    self.base_assert.except_error('点击忘记按钮后， 未进入单词听写页面')
                                self.spell_operate(right_answer, wrong_count=len(skip_index_info))

            bank_index[0] += 1
            if bank_id not in record_id_info[game_type]:
                record_id_info[game_type].append(bank_id)
            print('wrong:', wrong_index)
            print("skip:", skip_index_info)
            print('-' * 30, '\n')



