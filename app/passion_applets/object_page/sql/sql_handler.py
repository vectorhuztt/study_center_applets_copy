from app.passion_applets.object_page.sql.applet_sql import AppletSQL
from conf.decorator import teststep


class SqlHandler:
    def __init__(self):
        self.appletSql = AppletSQL()

    @classmethod
    def get_res_list(cls, res):
        return [x[0] for x in res] if res else []

    @teststep
    def get_wechat_user_id(self, username):
        result = self.appletSql.find_no_login_student_id(username)
        return result[0] if result else 0

    @teststep
    def get_available_first_label(self):
        """获取所有的已发布的一级标签"""
        result = self.appletSql.find_available_first_label()
        return self.get_res_list(result)

    @teststep
    def get_available_second_label(self, label_id):
        """获取一级标签下所有已发布的二级标签"""
        result = self.appletSql.find_available_second_label(label_id)
        return self.get_res_list(result)

    @teststep
    def get_label_books(self, label_id):
        """获取标签下的所有书籍"""
        result = self.appletSql.find_label_books(label_id)
        return self.get_res_list(result)

    @teststep
    def get_login_student_id_name(self, phone):
        """获取已登录学生id、name"""
        result = self.appletSql.find_login_student_id_name(phone)
        return result

    @teststep
    def get_login_student_school_name(self, student_id):
        """获取已登录学生学校名称"""
        result = self.appletSql.find_student_school(student_id)
        return result[0] if result else ''

    @teststep
    def get_book_related_label_id(self, book_id):
        result = self.appletSql.find_book_related_label_id(book_id)
        return result[0] if result else 0

    @teststep
    def get_book_unit_ids(self, book_label_id):
        """获取书籍的所有已激活的单元id"""
        result = self.appletSql.find_book_unit_label_id(book_label_id)
        return self.get_res_list(result)

    @teststep
    def get_book_word_count(self, unit_id_list):
        """获取书籍的单词个数"""
        result = self.appletSql.find_book_words_count(unit_id_list)
        return result[0] if result else 0

    @teststep
    def get_unit_word_count(self, unit_label_id):
        """获取书籍的单词个数"""
        result = self.appletSql.find_unit_word_count(unit_label_id)
        return result[0] if result else 0

    @teststep
    def get_book_today_review_count(self, student_id):
        """获取今天书籍复习单词数"""
        result = self.appletSql.find_book_today_review_word_count(student_id)
        return len(result[0].split(',')) if result else 0

    @teststep
    def get_student_map_school(self, student_id):
        """查询该学生已匹配的学校id"""
        result = self.appletSql.find_latest_student_map_school_id(student_id)
        return result[0] if result else 0

    @teststep
    def get_student_school_apply_status(self, student_id, school_id):
        """查询该学生是否已申请该学校"""
        result = self.appletSql.find_student_school_apply_record(student_id, school_id)
        return True if result else False

    @teststep
    def get_unit_studied_count(self, student_id, label_id, is_login=True):
        """获取单元已学次数"""
        result = self.appletSql.find_unit_already_studied_word_count(student_id, label_id)
        if not result:
            count = 0
        else:
            items_ids, complete_rate = result
            if not is_login:
                count = len(items_ids.split(','))
            else:
                if complete_rate == 100:
                    count = self.get_unit_word_count(label_id)
                else:
                    count = len(items_ids.split(','))
        return count






