import requests
import pickle
import os
from bs4 import BeautifulSoup
class Facebook:
    def __init__(self):
        headers={
            'method': 'POST',
            'scheme': 'https',
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }
        self.session = requests.session()
        self.session.headers.update(headers)

    def login(self, email, password):
        # get input field
        if os.path.isfile('cookie'):
            self.load_cookies()
        else:
            url = 'https://www.facebook.com/'
            req = self.session.get(url)
            soup = BeautifulSoup(req.text,'lxml')
            all_input_data = soup.find('form').findAll('input')
            data = {}
            for input_data in all_input_data:
                data[input_data.get('name')] = input_data.get('value')

            # input email and password
            data['email'] = email
            data['pass'] = password

            #login
            login_url = 'https://www.facebook.com/login'
            req = self.session.post(login_url,data=data)

            

        m_url = 'https://m.facebook.com/'
        req = self.session.get(m_url)
        soup = BeautifulSoup(req.text, 'lxml')
        all_input_data = soup.find('form',id='mbasic-composer-form').findAll('input')
        self.post_data = {}
        for input_data in all_input_data:
            self.post_data[input_data.get('name')] = input_data.get('value')
        try:
            self.fb_dtsg = soup.find('input',{'name':'fb_dtsg'}).get('value')
            self.save_cookies()
        except:
            print('username or password is invalid')

    def save_cookies(self):
        with open('cookie','wb') as f:
            pickle.dump(self.session.cookies, f)

    def load_cookies(self):
        with open('cookie','rb') as f:
            self.session.cookies.update(pickle.load(f))

    def post(self, content):
        post_url = 'https://m.facebook.com/composer/mbasic/'

        self.post_data['xc_message'] = content
        self.session.post(post_url, data=self.post_data)

    def get_post(self, post_id):
        post_url = 'https://m.facebook.com/story.php?story_fbid=%s&id=1'%str(post_id)
        return self.session.get(post_url).text

    def comment_post(self, post_id, comment):
        url = 'https://m.facebook.com/a/comment.php?fs=8&actionsource=2&comment_logging&ft_ent_identifier=%s'%str(post_id)
        comment = {'comment_text':comment,'fb_dtsg':self.fb_dtsg}
        self.session.post(url, data=comment)

    def comment_comment(self, comment_id):
        pass

    def like_post(self, post_id):
        pass

    def like_post_comment(self, post_id):
        pass

    def like_comment_comment(self, post_id):
        pass