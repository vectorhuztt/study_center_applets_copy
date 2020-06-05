import re


class ValidDate:

    WEEK_NAME = ['一', '二', '三', '四', '五', '六', '日']

    @classmethod
    def reform_date(cls, num, length=2):
        return '{:0>{}d}'.format(num, length)

    @classmethod
    def get_single_num_from_text(cls, text):
        """从文本中获取数字"""
        return int(re.findall(r'\d+', text)[0])

    @classmethod
    def get_multi_num_from_text(cls, text):
        """从文本中获取数字"""
        num_list = re.findall(r'\d+', text)
        return [int(x[0]) for x in num_list]