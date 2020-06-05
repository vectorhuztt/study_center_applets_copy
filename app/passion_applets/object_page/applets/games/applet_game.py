from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.common import CommonPage
from app.passion_applets.object_page.applets.games.flask_card import FlaskCardGame
from app.passion_applets.object_page.applets.games.word_choice import WordChoiceGame
from app.passion_applets.object_page.applets.games.word_macth import WordMatchGame
from app.passion_applets.object_page.applets.games.word_reform import ReformWordGame
from app.passion_applets.object_page.applets.games.word_spell import WordSpellGame
from conf.base_page import BasePage
from conf.decorator import teststep


class AppletGamePage(CommonPage):
    def __init__(self):
        super().__init__()
        self.word_choice = WordChoiceGame()

    @teststep
    def wait_check_game_page(self):
        """游戏界面检查点"""
        print('游戏页面\n')
        locator = (By.CSS_SELECTOR, '.Quiz-index--container')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_levels_page(self):
        """选择关卡页面检查点"""
        print('选择关卡页面\n')
        locator = (By.CSS_SELECTOR, '.level-wrapper')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def levels(self):
        """已通过关卡"""
        locator = (By.CSS_SELECTOR, '.level-skin')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def inactive_level(self):
        """未通过关卡"""
        locator = (By.CSS_SELECTOR, '.level-skin.inactive')
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def play_games_operate(self, do_right=False, is_review=False):
        """闯关游戏过程"""
        if self.wait_check_game_page():
            record_index = [0]
            spell_skip_info = []
            game_type_list = []
            study_info, word_info = {}, {}
            type_list = ['听音选词', '汉译英', '还原单词',  '单词拼写']
            record_id_info = {x: [] for x in type_list}
            wrong_index_info = {x: [] for x in type_list}
            right_word_info = {x: [] for x in type_list}
            while self.wait_check_game_page():
                game_container = self.game_container()

                if 'SK' in game_container:   # 闪卡录音游戏
                    FlaskCardGame().flask_game_operate(study_info, is_review)
                    word_info = {x: study_info[x] for x in study_info if study_info[x]['bank_type'] == '单词'}

                elif 'LLK' in game_container:
                    WordMatchGame().word_match_operate(study_info)

                elif 'CHXZ' in game_container:
                    game_mode = 'TX' if self.word_choice.hidden_right_word_explain() else "HY"
                    if game_mode == 'TX':    # 听音选词
                        game_type = type_list[0]
                    else:
                        game_type = type_list[1]
                    game_type_list.append(game_type)
                    wrong_index = wrong_index_info[game_type]
                    right_info = right_word_info[game_type]
                    WordChoiceGame().word_choice_game_operate(game_mode, study_info, do_right=do_right,
                                                              bank_index=record_index, wrong_index=wrong_index,
                                                              right_info=right_info, record_id_info=record_id_info,
                                                              type_list=game_type_list, word_count=len(word_info),
                                                              is_review=is_review)

                elif 'HYDC' in game_container:
                    game_type = type_list[2]
                    game_type_list.append(game_type)
                    wrong_index = wrong_index_info[game_type]
                    right_info = right_word_info[game_type]
                    ReformWordGame().reform_word_game_operate(word_info, do_right=do_right,
                                                              bank_index=record_index, wrong_index=wrong_index,
                                                              right_info=right_info, record_id_info=record_id_info,
                                                              type_list=game_type_list, word_count=len(word_info),
                                                              is_review=is_review)

                elif 'DCPX' in game_container:
                    game_type = type_list[3]
                    game_type_list.append(game_type)
                    wrong_index = wrong_index_info[game_type]
                    right_info = right_word_info[game_type]
                    WordSpellGame().spell_word_game_operate(study_info, do_right=do_right,
                                                            bank_index=record_index, wrong_index=wrong_index,
                                                            right_info=right_info, skip_index_info=spell_skip_info,
                                                            record_id_info=record_id_info, type_list=game_type_list,
                                                            word_count=len(word_info), is_review=is_review)
                else:
                    break
            if not do_right:
                print(wrong_index_info)
                self.wrong_index_check_operate(is_review, word_count=len(word_info),
                                               wrong_index_info=wrong_index_info, spell_skip_info=spell_skip_info)

    @teststep
    def wrong_index_check_operate(self, is_review, *, word_count,  wrong_index_info, spell_skip_info):
        """错题索引间隔判断"""
        if not is_review:
            listen_choice_index = wrong_index_info['听音选词']
            check_listen_choice_index = [listen_choice_index[0] + 2*x for x in range(5)]
            if listen_choice_index != check_listen_choice_index:
                self.base_assert.except_error('听音选词的错题顺序不正确, 应为{}, 实际为{}'
                                              .format(str(check_listen_choice_index), str(listen_choice_index)))
            hans_choice_index = wrong_index_info['汉译英']
            check_hans_choice_index = [hans_choice_index[0] + 2*x for x in range(5)]
            if hans_choice_index != check_hans_choice_index:
                self.base_assert.except_error('听音选词的错题顺序不正确, 应为{}, 实际为{}'
                                              .format(str(check_hans_choice_index), str(hans_choice_index)))

            check_skip_index = [spell_skip_info[0] + 2 * x for x in range(5)]
            if spell_skip_info != check_skip_index:
                self.base_assert.except_error('单词拼写的跳过顺序不正确, 应为{}, 实际为{}'
                                              .format(str(check_skip_index), str(spell_skip_info)))

        if word_count:
            word_reform_index = wrong_index_info['还原单词']
            check_reform_index = [word_reform_index[0] + 2*x for x in range(5)]
            if word_reform_index != check_reform_index:
                self.base_assert.except_error('还原单词的错题顺序不正确, 应为{}, 实际为{}'
                                              .format(str(word_reform_index), str(check_reform_index)))

        word_spell_index = wrong_index_info['单词拼写']
        check_spell_index = [word_spell_index[0] + 2*x for x in range(5)]
        if word_spell_index != check_spell_index:
            self.base_assert.except_error('单词拼写的错题顺序不正确, 应为{}, 实际为{}'
                                          .format(str(check_spell_index), str(word_spell_index)))










