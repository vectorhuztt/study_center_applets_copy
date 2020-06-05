import json
import os
import yaml
current_path = os.path.abspath(os.path.dirname(__file__))
yaml_path = current_path.split('app\\')[0] + 'conf\\user_info.yaml'
yaml_info = json.dumps(yaml.load(open(yaml_path, 'r', encoding='utf-8').read(), Loader=yaml.FullLoader))
user_info = json.loads(yaml_info)['userinfo']


class Account:
    def __init__(self):
        self.valid_account = user_info['AnyPhone']
        self.login_accounts = user_info['CheckLogin']

    def account(self):
        return self.valid_account['userphone']

    def password(self):
        return self.valid_account['userpwd']