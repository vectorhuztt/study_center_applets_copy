import time

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.common import CommonPage
from conf.decorator import teststep


class FlaskCardGame(CommonPage):
    @teststep
    def flask_word(self):
        """闪卡单词"""
        locator = (By.CSS_SELECTOR, ".SK-index--word")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def flask_voice(self):
        """闪卡声音"""
        locator = (By.CSS_SELECTOR, ".SK-index--circle-button-voice")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def flask_explain(self):
        """闪卡解释"""
        locator = (By.CSS_SELECTOR, ".SK-index--explain")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def flask_sentence(self):
        """闪卡句子"""
        locator = (By.CSS_SELECTOR, ".SK-index--en")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def flask_sentence_explain(self):
        """闪卡句子解释"""
        locator = (By.CSS_SELECTOR, ".SK-index--zh")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def flask_voice_play_btn(self):
        """闪卡播放按钮"""
        locator = (By.CSS_SELECTOR, ".SK-index--circle-button-voice")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def flask_voice_record_btn(self):
        """闪卡录音按钮"""
        locator = (By.CSS_SELECTOR, ".SK-index--circle-button-record")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def flask_voice_recording_btn(self):
        """闪卡正在录音按钮"""
        locator = (By.CSS_SELECTOR, ".SK-index--recording")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def flask_play_record_voice_btn(self):
        """录音播放按钮"""
        locator = (By.CSS_SELECTOR, '.SK-index--circle-button-play')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def flask_next_btn(self):
        """闪卡下一步按钮"""
        locator = (By.CSS_SELECTOR, ".SK-index--quiz-button")
        return self.get_wait_check_page_ele(locator, timeout=5)

    @teststep
    def flask_game_operate(self, word_info, is_review):
        print('---- 闪卡游戏 ----\n')
        bank_count = self.bank_count()
        for x in range(bank_count):
            if not is_review:
                self.btn_status_judge(self.flask_play_record_voice_btn)
                self.next_btn_isvisible_judge(self.flask_next_btn)
                if self.flask_next_btn():
                    self.base_assert.except_error('默认显示下一题按钮')
            self.current_index_judge(x+1)
            bank_id = self.game_id()
            word_info[bank_id] = {}
            word = self.flask_word().text
            word_explain = self.flask_explain().text
            word_type = "短语" if ' ' in word else '单词'
            print('单词id：', bank_id)
            print('单词：', word)
            print('解释：', word_explain)
            print('句子：', self.flask_sentence().text)
            print("句子解释：", self.flask_sentence_explain().text,)
            word_info[bank_id] = {'word': word, 'explain': word_explain, 'bank_type': word_type}

            if not is_review:
                self.flask_voice().click()
                self.flask_voice_record_btn().click()
                if x == 0:
                    time.sleep(21)
                    self.next_btn_isvisible_judge(self.flask_next_btn, is_visible=True)
                    self.btn_status_judge(self.flask_play_record_voice_btn, flag=True)
                else:
                    time.sleep(3)
                    self.flask_voice_recording_btn().click()
                    time.sleep(2)
            self.next_btn_operate(self.flask_next_btn)
            print('-'*30, '\n')
            time.sleep(5)