import time

from selenium.webdriver.common.by import By

from app.passion_applets.object_page.applets.books.books_page import BooksPage
from app.passion_applets.object_page.applets.common import CommonPage
from app.passion_applets.object_page.applets.user_center.account_page import SchoolPage
from app.passion_applets.object_page.applets.user_center.apply_school import ApplySchoolPage
from app.passion_applets.test_data.account import Account
from conf.decorator import teststep


class MineTabPage(CommonPage):

    @teststep
    def wait_check_mine_tab_page(self):
        """个人中心页面检查点"""
        locator = (By.CSS_SELECTOR, '.account')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wechat_nickname(self):
        """用户名称"""
        locator = (By.CSS_SELECTOR, '.nick-name wx-open-data')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def user_score(self):
        """用户积分"""
        locator = (By.CSS_SELECTOR, '.integral-wrapper wx-text span:not([style="display:none;"]) .integral')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def mine_school(self):
        """我的学校"""
        locator = (By.CSS_SELECTOR, 'wx-button:nth-child(1) .school')
        return self.get_wait_check_page_ele(locator)
    
    @teststep
    def mine_school_btn(self):
        """我的学校"""
        locator = (By.CSS_SELECTOR, 'wx-button:nth-child(1)')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def current_study_book(self):
        """当前学习书籍"""
        locator = (By.CSS_SELECTOR, 'wx-button:nth-child(2) .school')
        return self.get_wait_check_page_ele(locator)
    
    @teststep
    def study_book_btn(self):
        """当前学习课程按钮"""
        locator = (By.CSS_SELECTOR, 'wx-button:nth-child(2)')
        return self.get_wait_check_page_ele(locator)
    
    @teststep
    def bind_student_btn(self):
        """绑定百项过学生端按钮"""
        locator = (By.CSS_SELECTOR, 'wx-button:nth-child(3)')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def wait_check_student_login_page(self):
        """学生登录页面检查点"""
        locator = (By.CSS_SELECTOR, '.login')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def account_input(self):
        """账号输入框"""
        locator = (By.CSS_SELECTOR, 'wx-input:nth-child(1)')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def password_input(self):
        """密码输入栏"""
        locator = (By.CSS_SELECTOR, 'wx-input:nth-child(2)')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def login_btn(self):
        """登录按钮"""
        locator = (By.CSS_SELECTOR, '.login-btn')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def hint_view(self):
        """登录下方申请加入学习提示"""
        locator = (By.CSS_SELECTOR, '.hint')
        return self.get_wait_check_page_ele(locator)

    @teststep
    def change_book_operate(self):
        """重新选择书籍"""
        if self.wait_check_mine_tab_page():
            self.study_book_btn().click()
            book_info = BooksPage().select_label_books_operate()
            if self.wait_check_mine_tab_page():
                mine_tab_book_name = self.current_study_book().text
                if book_info['book_name'] != mine_tab_book_name:
                    self.base_assert.except_error('重新选择书籍后，个人中心的课程名与所选书籍名称不一致')

    @teststep
    def login_form_operate(self, phone, password, *, phone_clear_length=0, pwd_clear_length=0,
                           is_error=False, assert_text=None):
        """
        登录表单操作
        :param phone:  手机号
        :param password: 密码
        :param assert_text: 错误提示
        :param is_error: 是否错误
        :param phone_clear_length: 手机号清除内容长度
        :param pwd_clear_length: 密码清除内容长度
        :return:
        """
        self.account_input().click()
        self.wechat.app_page_login_account(phone, clear_length=phone_clear_length)
        self.password_input().click()
        self.wechat.app_page_login_password(password, assert_text=assert_text,
                                            is_check=is_error, clear_length=pwd_clear_length)
        time.sleep(2)

    @teststep
    def login_operate(self, is_check=False):
        """登录操作"""
        if self.wait_check_mine_tab_page():
            self.mine_school_btn().click()
            self.wechat.handle_alert_tip(allow=False)
            if self.wait_check_student_login_page():
                account = Account()
                check_accounts = account.login_accounts
                if is_check:
                    for i, x in enumerate(check_accounts):
                        phone_clear_length = len(check_accounts[i-1]['phone']) if i != 0 else 0
                        pwd_clear_length = len(check_accounts[i-1]['password']) if i!= 0 else 0
                        print('账号:', x['phone'])
                        print('密码:', x['password'])
                        self.login_form_operate(x['phone'], x['password'], is_error=True,
                                                assert_text=x['assert'], phone_clear_length=phone_clear_length,
                                                pwd_clear_length=pwd_clear_length)

                phone = account.account()
                password = account.password()
                user_id, username = self.sql_handler.get_login_student_id_name(phone)
                school_name = self.sql_handler.get_login_student_school_name(user_id)
                student_info = {
                    'id': user_id,
                    'username': username,
                    'userphone': str(phone),
                    'school_name': school_name
                }
                print('学生账号：', str(phone))
                print('学生密码：', password)
                print('学生id：', user_id)
                print('学名称：', school_name, '\n')

                self.login_form_operate(phone, password, phone_clear_length=len(account.login_accounts[-1]['phone']),
                                        pwd_clear_length=len(account.login_accounts[-1]['password']))
                if not self.wait_check_mine_tab_page():
                    self.base_assert.except_error('点击登录后未重新进入个人中心页面')
                else:
                    school_btn = self.mine_school_btn()
                    bind_student_btn = self.bind_student_btn()
                    if '暂未绑定' in school_btn.text:
                        self.base_assert.except_error('已成功登陆, 学校按钮文本未显示学校名称')
                    if '已成功绑定' not in bind_student_btn.text:
                        self.base_assert.except_error('已成功登陆， 但是绑定按钮文本未显示为已成功绑定')
                return student_info
            return None

    @teststep
    def logout_operate(self, student_info):
        """退出操作"""
        if self.wait_check_mine_tab_page():
            self.bind_student_btn().click()
            SchoolPage().account_page_operate(student_info)
            # 退出登录后页面内容校对
            if not self.wait_check_mine_tab_page():
                self.base_assert.except_error('点击退出登录， 未重新进入个人中心页面')
            else:
                school_btn = self.mine_school_btn()
                bind_student_btn = self.bind_student_btn()
                if '暂未绑定' not in school_btn.text:
                    self.base_assert.except_error('已退出登陆, 学校按钮文本未显示暂未绑定文本')
                if '绑定百项过' not in bind_student_btn.text:
                    self.base_assert.except_error('已退出登陆， 但是绑定按钮文本未显示为绑定学生端')

    @teststep
    def apply_school_operate(self):
        """申请学校操作"""
        if self.wait_check_mine_tab_page():
            nickname = self.wechat_nickname().text
            wechat_user_id = self.sql_handler.get_wechat_user_id(nickname)
            print('微信名称：', nickname)
            print('微信用户id：', wechat_user_id)
            self.mine_school_btn().click()
            self.wechat.handle_alert_tip(allow=False)
            if self.wait_check_student_login_page():
                self.hint_view().click()
                flag = ApplySchoolPage().apply_school_operate(wechat_user_id)
                if not flag:
                    if self.wait_check_student_login_page():
                        self.hint_view().click()
                        ApplySchoolPage().apply_school_operate(wechat_user_id)
                if self.wait_check_student_login_page():
                    self.click_applet_back_btn()
                    if self.wait_check_mine_tab_page():
                        self.click_applet_back_btn()





