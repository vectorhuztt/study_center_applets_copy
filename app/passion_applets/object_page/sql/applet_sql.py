from utils.sql import SqlDb


class AppletSQL(SqlDb):

    def find_no_login_student_id(self, student_name):
        """获取学生id"""
        sql = "select id from `user` where phone=0 and `name`='{}' " \
              "and user_type_id=6 and deleted_at is NULL".format(student_name)
        return self.execute_sql_return_result(sql, single=True)

    def find_login_student_id_name(self, phone):
        """查询已登录学生id"""
        sql = "select id, `name` from `user` where phone={} and user_type_id=2".format(phone)
        return self.execute_sql_return_result(sql, single=True)

    def find_student_school(self, student_id):
        """查询已登录学生id"""
        sql = "select school.name from school, statistic_student_record as ssr " \
              "where school.id=ssr.school_id and ssr.student_id={}".format(student_id)
        return self.execute_sql_return_result(sql, single=True)

    def find_available_first_label(self):
        """获取已发布的一级标签"""
        sql = "select id from label where is_available=1"
        return self.execute_sql_return_result(sql)

    def find_available_second_label(self, label_id):
        """获取已发布的二级标签"""
        sql = 'select id from label where parent_id={} and is_available=1'.format(label_id)
        return self.execute_sql_return_result(sql)

    def find_label_books(self, label_id):
        """获取标签下的书籍"""
        sql = "select id from course_book where label_id={}".format(label_id)
        return self.execute_sql_return_result(sql)

    def find_book_related_label_id(self, book_id):
        """获取书籍对应的标签id"""
        sql = "SELECT core_label_id FROM word_book_core_label_map where book_id={}".format(book_id)
        return self.execute_sql_return_result(sql, single=True)

    def find_book_unit_label_id(self, book_label_id):
        """查询书籍下所有单元的id"""
        sql = "SELECT id from core_label WHERE  is_active=1 and deleted_at is NULL and " \
              "parent_id = {}".format(book_label_id)
        return self.execute_sql_return_result(sql)

    def find_book_words_count(self, label_ids):
        """查询书籍的单词个数(不去重)"""
        sql = "select COUNT(id) from wordbank_translation_label where label_id in {}".format(str(tuple(label_ids)))
        return self.execute_sql_return_result(sql, single=True)

    def find_unit_word_count(self, label_id):
        """查询单元单词个数"""
        sql = "select COUNT(id) from wordbank_translation_label where label_id = {}".format(label_id)
        return self.execute_sql_return_result(sql, single=True)

    def find_unit_already_studied_word_count(self, student_id, label_id):
        """查询单元已学的单词个数"""
        sql = "SELECT item_ids, completion_rate from word_student_record where " \
              "student_id = {} and object_id = {} ".format(student_id, label_id)
        return self.execute_sql_return_result(sql, single=True)

    def find_book_today_review_word_count(self, student_id):
        """查询书籍今日复习个数"""
        sql = 'SELECT `value` FROM word_student_data WHERE student_id = {} and `key`="review_translation_ids" ' \
              'and DATEDIFF(now(), updated_at) = 0 ORDER BY updated_at desc'.format(student_id)
        return self.execute_sql_return_result(sql, single=True)

    def  find_latest_student_map_school_id(self, student_id):
        """查询学生最新的匹配的学校id"""
        sql = "SELECT school_id from school_user_position_map WHERE user_id = {} " \
              "ORDER BY `id` desc LIMIT 1".format(student_id)
        return self.execute_sql_return_result(sql, single=True)

    def find_student_school_apply_record(self, student_id, school_id):
        """查询学生的学校申请记录"""
        sql = "SELECT id from school_application WHERE user_id = {} and " \
              "school_id = {} and deleted_at is null".format(student_id, school_id)
        print(sql)
        return self.execute_sql_return_result(sql, single=True)
