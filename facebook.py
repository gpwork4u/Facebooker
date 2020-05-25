import requests
import pickle
import os
from bs4 import BeautifulSoup
def letter_adder(string, num):
    if ord(string[1]) + num%26 >= ord('z'):
        string = chr(ord(string[0])+1) + chr(ord(string[1])+ num - 26)
    else:
        string = string[0] + chr(ord(string[1]) + num)
    return string

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

            
        # get hidden input data
        url = 'https://m.facebook.com/'
        req = self.session.get(url)
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
        url = 'https://m.facebook.com/composer/mbasic/'
        self.post_data['xc_message'] = content
        self.session.post(url, data=self.post_data)

    def get_post(self, post_id):
        url = 'https://m.facebook.com/story.php?story_fbid=%s&id=1'%str(post_id)
        req = self.session.get(url)
        soup = BeautifulSoup(req.text,'lxml')
        post_content = soup.find(id='objects_container').string
        return post_content
    
    def get_comments(self, post_id, p=0):
        url = 'https://m.facebook.com/story.php?story_fbid=%s&id=1&p=%s'%(str(post_id),p)
        req = self.session.get(url)
        soup = BeautifulSoup(req.text,'lxml')
        div = soup.find('div',id='ufi_%s'%str(post_id))
        comment_div = div.find('div',id='sentence_%s'%str(post_id)).next_sibling
        class1 = comment_div.get('class')[0]
        comment_class = letter_adder(class1, 1)
        comments = comment_div.findAll('div', recursive=False, class_=comment_class)
        content_class = letter_adder(class1, 4)

        pre_page_div = comment_div.find('div', id='see_prev_%s'%str(post_id))
        if pre_page_div:
            pre_href = pre_page_div.find('a').get('href')
            pre_href = pre_href[pre_href.find('p='):]
            page = pre_href[2:pre_href.find('&')]
            ret = self.get_comments(post_id, p=page)
            comments_id = ret[0]
            users = ret[1]
            comments_contents = ret[2]
            comments_time = ret[3]
        else:
            comments_id = []
            users = []
            comments_contents = []
            comments_time = []
        for comment in comments:
            try:
                users.append(comment.find('h3').text)
                comments_id.append(comment.get('id'))
                comments_contents.append(comment.find('h3').next_sibling.text)
                comments_time.append(comment.find('abbr').text)
            except:
                print('error')

        return comments_id, users, comments_contents, comments_time

    def get_likes(self, post_id):
        pass
    
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