import re
import time

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.common import CommonPage
from conf.decorator import teststep


class WordMatchGame(CommonPage):

    @teststep
    def wait_check_word_match_page(self):
        """连连看游戏页面检查点"""
        locator = (By.CSS_SELECTOR, '.LLK-index--grid')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def card_item(self):
        """连连看卡片"""
        locator = (By.CSS_SELECTOR, '.LLK-index--grid-item-content')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def get_card_item_class(self, index):
        locator = (By.XPATH, '//wx-text[@class="LLK-index--grid-item-content"]/..')
        ele = self.get_wait_check_page_ele(locator, single=False)
        return ele[index].get_attribute('class')

    @teststep
    def is_hans(self, word):
        """判断 是否为字母"""
        pattern = re.compile(u'[\u4e00-\u9fa5]+')
        if pattern.search(word):
            return True
        else:
            return False

    @teststep
    def get_hans_en_cards(self, hans=False):
        """获取中文/英文卡片"""
        cards = []
        card_list = self.card_item()
        for i, x in enumerate(card_list):
            if hans:
                if self.is_hans(x.text):
                    cards.append((x, i))
            else:
                if not self.is_hans(x.text):
                    cards.append((x, i))
        return cards

    @teststep
    def word_match_operate(self, study_info):
        print('----  连连看游戏  ----\n')
        right_answer = {}
        while self.wait_check_word_match_page():
            for x in study_info:
                word_info = study_info[x]
                word = word_info['word']
                explain = word_info['explain']
                right_answer[word] = explain
            en_cards = self.get_hans_en_cards()
            zh_cards = self.get_hans_en_cards(hans=True)

            right_list = []
            for en in en_cards:
                word_explain = right_answer[en[0].text]
                en[0].click()
                select_zh_info = 0
                for zh in zh_cards:
                    if zh[0].text == word_explain:
                        select_zh_info = (zh[0].text, zh[1])
                        print('单词：', en[0].text)
                        print('解释：', zh[0].text)
                        zh[0].click()
                        right_list.append(en[0])
                        time.sleep(1)
                        break
                if len(right_list) < len(en_cards):
                    if 'destroy' not in self.get_card_item_class(en[1]):
                        self.base_assert.except_error('已选择正确答案, 该英文卡片未消失, 单词： %s' % en[0].text)
                    if 'destroy' not in self.get_card_item_class(select_zh_info[1]):
                        self.base_assert.except_error('已选择正确答案, 该中文文卡片未消失, 单词： %s' % select_zh_info[0])
                else:
                    time.sleep(5)
                print('-'*30, '\n')

