#Encoding=UTF8

import tornado.web
import MongoHelper
import json
import Utils
import BaseAuthenticateHandler

class SearchHandler(BaseAuthenticateHandler.BaseAuthenticateHandler):
    def post(self):
        result = {'status': False}
        try:
            user_id = self.get_argument('user_id', '')
            raw = self.get_argument('raw', '')
            # 我_r 想_v 找_v 去年_nt 夏天_nt 在_p 西雅图_ns 农贸市场_n 的_u 照片_n
            
        ######added by peigang###
            token = self.get_argument('token','')
            user = MongoHelper.get_user_by_id(user_id)
            if token != user['token']:
                return
        ######added by peigang###
            if user_id == '' or raw == '':
                return
            
            key_words = raw.split(' ')
            if key_words is None or len(key_words) == 0:
                return
            
            meaningful = Utils.get_meaningful_keywords(key_words)
            image  = Utils.get_images_by_tag(user_id, meaningful)
            result['status'] = True
            result['image'] = image['image_name']
            
        finally:
            self.write(json.dumps(result))
