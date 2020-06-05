import re

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.games.result_page import ResultPage
from conf.base_page import BasePage
from conf.decorator import teststep


class RankPage(BasePage):

    @teststep
    def wait_check_rank_page(self):
        """排行页面检查点"""
        locator = (By.CSS_SELECTOR, '.rank-list')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_user_medal(self, ele):
        """判断用户是否有奖牌显示"""
        try:
            ele.find_element_by_css_selector('.medal')
            return True
        except:
            return False

    @teststep
    def wait_check_share_img(self):
        """分享图页面检查点"""
        locator = (By.CSS_SELECTOR, '.share-image')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def current_user_name(self):
        """当前用户的昵称"""
        locator = (By.CSS_SELECTOR, ".rank-list .user .right span")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def current_user_score(self):
        """当前用户的积分"""
        locator = (By.CSS_SELECTOR, ".rank-list .user .gold")
        score = self.get_wait_check_page_ele(locator).text
        return int(re.search(r'\d+', score).group())

    @teststep
    def current_user_rank(self):
        """当前用户排行"""
        locator = (By.CSS_SELECTOR, ".rank-list .user .ranking")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def invite_friend_btn(self):
        """邀请好友"""
        locator = (By.CSS_SELECTOR, ".rank-list .user .invite")
        return self.get_wait_check_page_ele(locator)

    @teststep
    def last_rank_user_score(self):
        """排行最后一个"""
        locator = (By.CSS_SELECTOR, ".rank-list .rank-item:last-child .gold")
        score = self.get_wait_check_page_ele(locator).text
        return int(re.search(r'\d+', score).group())

    @teststep
    def rank_user_count(self):
        """排行中用户个数"""
        locator = (By.CSS_SELECTOR, ".rank-list .rank-item")
        return self.get_wait_check_page_ele(locator, single=False)

    @teststep
    def rank_data_check_operate(self, username):
        """排行榜页面 数据校验"""
        rank_username = self.current_user_name().text
        if rank_username != username:
            self.base_assert.except_error("页面用户名称与个人中心的名称不一致")
        last_user_score = self.last_rank_user_score()
        current_user_score = self.current_user_score()
        current_user_rank = self.current_user_rank().text

        if current_user_score > last_user_score:
            if '未上榜' in current_user_rank:
                self.base_assert.except_error('当前用户积分比排行榜最后一名多， 但是显示未上榜')

        rank_users = self.rank_user_count()
        print('当前页面排行用户数：', len(rank_users))
        if len(rank_users) != 50:
            self.base_assert.except_error('当前排行人数不为50人')

        for x in rank_users[:3]:
            if not self.wait_check_user_medal(x):
                self.base_assert.except_error('当前用户处于第三名， 但是未发现对应奖牌')

        self.invite_friend_btn().click()
        if self.wait_check_share_img():
            ResultPage().share_image_operate()
        if not self.wait_check_rank_page():
            self.base_assert.except_error('保存分享图片后, 未重新进入排行榜页面')


