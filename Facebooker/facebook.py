import requests
import pickle
import os
import logging
import time
import json
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder

def letter_adder(string, num):
    if ord(string[1]) + num%26 >= ord('z'):
        string = chr(ord(string[0])+1) + chr(ord(string[1])+ num - 26)
    else:
        string = string[0] + chr(ord(string[1]) + num)
    return string

class API:
    '''
    FB post structure:
        post
        |
        --comment
            |
            --reply
    '''
    def __init__(self):
        headers={
            'scheme': 'https',
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',
            'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) ' + \
                         'Gecko/20100101 Firefox/76.0',
        }
        self.session = requests.session()
        self.session.headers.update(headers)
        self.login_check = False
    def login(self, email, password):
        # get input field
        self.session.cookies.clear()
        if os.path.isfile(email+'.cookie'):
            self.__load_cookies(email+'.cookie')
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
        self.user_id = self.session.cookies.get_dict()['c_user']
        # get hidden input data
        url = 'https://m.facebook.com/'
        req = self.session.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        try:
            self.fb_dtsg = soup.find('input', {'name':'fb_dtsg'}).get('value')
        except Exception as e:
            logging.debug(e)
            logging.error('username or password is invalid')
            return False
        
        self.login_check = True
        self.__save_cookies(email+'.cookie')
        self.post_to_user_data = {
                                    'fb_dtsg':self.fb_dtsg,
                                    'xhpc_timeline':'1',
                                    'c_src':'timeline_other',
                                    'cwevent':'composer_entry',
                                    'referrer':'timeline',
                                    'ctype':'inline',
                                    'cver':'amber',
                                    'rst_icv':None,
                                    'view_post':'view_post'
                                 }
                                    
        self.post_data = {
                            'fb_dtsg': self.fb_dtsg,
                            'privacyx': '291667064279714',
                            'target': self.user_id,
                            'c_src': 'feed',
                            'cwevent': 'composer_entry',
                            'referrer': 'feed',
                            'ctype': 'inline',
                            'cver': 'amber',
                            'rst_icv': None,
                            'view_post': 'view_post',
                         }
        self.send_msg_data = {
                                'fb_dtsg': self.fb_dtsg,
                                'body':'',
                                'send':'傳送',
                                'wwwupp':'C3'
                              }

    def __save_cookies(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.session.cookies, f)

    def __load_cookies(self, filename):
        with open(filename,'rb') as f:
            self.session.cookies.update(pickle.load(f))
    
    # post methods
    def get_post(self, post_id):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = 'https://m.facebook.com/story.php?' + \
              'story_fbid=%s&id=1'%str(post_id)
        req = self.session.get(url)
        soup = BeautifulSoup(req.text,'lxml')
        post_content = soup.find('div',class_='z')
        if not post_content:
            logging.error('This post is not supported or you don\'t have acess authority')
        return post_content

    def like_post(self, action, post_id):
        '''
            action:
                0 : like
                1 : Love
                2 : Care
                3 : Haha
                4 : Wow
                5 : Sad
                6 : Angry
        '''

        if not self.login_check:
            logging.error('You should login first')
            return
        if action > 6 or action < 0:
            logging.error('This action is not supported')
            return
        url = 'https://m.facebook.com/reactions/picker/?ft_id=' + str(post_id)
        req = self.session.get(url)
        try:
            soup = BeautifulSoup(req.text, 'lxml')
            root = soup.find('div', id='root').find('table', role='presentation')
            action_href = [a.get('href')  for a in root.findAll('a')][:-1]
            like_url = 'https://m.facebook.com' + action_href[action]
            self.session.get(like_url)
        except:
            logging.error('You don\'t have access authority')

    def get_user_post_list(self, user_id, num=10):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = 'https://m.facebook.com/profile/timeline/stream/?' + \
              'end_time=%s&'%str(time.time()) + \
              'profile_id=%s'%str(user_id)
        posts_id = []
        while len(posts_id) < num:
            req = self.session.get(url)
            soup = BeautifulSoup(req.text, 'lxml')
            posts = soup.find('section').findAll('article', recursive=False)
            for post in posts:
                data = json.loads(post.get('data-ft'))
                post_id = data['mf_story_key']
                posts_id.append(post_id)
                if len(posts_id) >= num:
                    break
            if len(posts_id) >= num:
                    break
            next_href = soup.find('div', id='u_0_0').find('a').get('href')
            url = 'https://m.facebook.com' + next_href
        return posts_id


    def post(self, content, privacy_level=0, user_id=None):
        if not self.login_check:
            logging.error('You should login first')
            return
        public = 300645083384735 # level 0
        freind = 291667064279714 # level 1
        privacy = [public, freind]
        url = 'https://m.facebook.com/composer/mbasic/'
        self.post_data['xc_message'] = content
        if user_id:
            self.post_to_user_data['target'] = user_id
            self.post_to_user_data['id'] = user_id
            self.post_to_user_data['xc_message'] = content
            self.session.post(url, data=self.post_to_user_data)
        else:
            self.post_data['privacyx'] = privacy[privacy_level]
            self.post_data['xc_message'] = content
            self.session.post(url, data=self.post_data)

    def fanpage_post(self, content, fanpage_id):
        if not self.login_check:
            logging.error('You should login first')
            return
        fanpage_id = str(fanpage_id)
        url = 'https://m.facebook.com/composer/mbasic/?c_src=page_self' + \
              '&referrer=pages_feed' + \
              '&target=%s&cwevent=composer_entry&av=%s'%(fanpage_id,fanpage_id)
        req = self.session.get(url)
        soup = BeautifulSoup(req.text,'lxml')
        form = soup.find('form', id='composer_form')
        input_datas = form.findAll('input')
        data = {}
        for input_data in input_datas:
            data[input_data.get('name')] = input_data.get('value')
        action = form.get('action')
        data['xc_message'] = content
        mp_encoder = MultipartEncoder(
            fields = data
        )
        self.session.post(url,
                          data=mp_encoder,
                          headers={'Content-Type': mp_encoder.content_type})
    # comment methods
    def get_comments(self, post_id, num=10, start=0):
        if not self.login_check:
            logging.error('You should login first')
            return
        
        comments_id = []
        users = []
        comments_contents = []
        comments_time = []
        while num > 0:
            url = 'https://m.facebook.com/story.php?' + \
                'story_fbid=%s&id=1&p=%s'%(str(post_id),start)
            req = self.session.get(url)
            soup = BeautifulSoup(req.text,'lxml')
            try:
                div = soup.find('div',id='ufi_%s'%str(post_id))
                comment_div = div.find('div',id='sentence_%s'%str(post_id)).next_sibling
                comments = comment_div.findAll('div', recursive=False)
                comments.reverse()
            except Exception as e:
                logging.debug(e)
                logging.error('You don\'t have access authority')
                return
            for comment in comments:
                try:
                    users.append(comment.find('h3').text)
                    comments_id.append(comment.get('id'))
                    comments_contents.append(comment.find('h3').next_sibling.text)
                    comments_time.append(comment.find('abbr').text)
                    num -= 1
                except:
                    pass

            pre_page_div = comment_div.find('div', id='see_prev_%s'%str(post_id))

            if pre_page_div:
                pre_href = pre_page_div.find('a').get('href')
                pre_href = pre_href[pre_href.find('p='):]
                start = pre_href[2:pre_href.find('&')]
            else:
                break



        return list(zip(comments_id, users, comments_contents, comments_time))

    def delete_comment(self, post_id, comment_id):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = 'https://m.facebook.com/ufi/delete/?' + \
              'delete_comment_id=%s'%str(comment_id) + \
              '&delete_comment_fbid=%s'%str(comment_id) + \
              '&ft_ent_identifier=%s'%str(post_id)
        data = {'fb_dtsg': self.fb_dtsg}
        return self.session.post(url, data=data)

    def comment(self, post_id, content):
        url = 'https://m.facebook.com/a/comment.php?' + \
              'fs=8&actionsource=2&comment_logging' + \
              '&ft_ent_identifier=%s'%str(post_id)
        comment = {'comment_text':content,'fb_dtsg':self.fb_dtsg}
        return self.session.post(url, data=comment)

    # reply method
    def reply(self, post_id ,comment_id, content):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = 'https://m.facebook.com/a/comment.php?' + \
              'parent_comment_id=%s'%str(comment_id) + \
              '&ft_ent_identifier=%s'%str(post_id)
        data = {'fb_dtsg': self.fb_dtsg, 'comment_text':content}
        self.session.post(url, data=data)

    # messenger method
    def get_msg(self, chat_room_id, num=1):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = 'https://m.facebook.com/messages/read/?tid=%s'%str(chat_room_id)
        send_from = []
        content = []
        time = []
        while num > 0:
            req = self.session.get(url)
            soup = BeautifulSoup(req.text, 'lxml')
            msg_group = soup.find('div', id='messageGroup')
            if len(msg_group) == 1:
                index = 0
            else:
                index = 1
            
            msgs = msg_group.findAll('div', recursive=False)[index].findAll('div', recursive=False)
            if msgs:
                msgs.reverse()
            for msg in msgs:
                content_class = letter_adder(msg.get('class')[-1], 1)
                try:
                    msg_contents = msg.find('div', class_=content_class). \
                                                        find('div').findAll('span')
                    for msg_content in msg_contents:
                        send_from.append(msg.find('strong').text)
                        content.append(msg_content.text)
                        time.append(msg.find('abbr').text)
                        num -= 1
                        if num <= 0:
                            break
                    if num <= 0:
                        break
                except:
                    logging.debug('Get non text message')
                    pass
            pre_page = msg_group.find('div', id='see_older')
            if not pre_page:
                break
            href = pre_page.find('a').get('href')
            url = 'https://m.facebook.com' + href

        return list(zip(send_from, content, time))

    def get_unread_chat(self):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = 'https://m.facebook.com/messages/?folder=unread'
        req = self.session.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        unread_chats = soup.find('div', id='root').find('section').findAll('table')
        unread_chat_room_id = []
        for unread_chat in unread_chats:
            href = unread_chat.find('a').get('href')
            if href.find('cid.c') >= 0:
                chat_room_id = href[href.find('cid.c.')+6:href.find('%')]
                if chat_room_id == self.user_id:
                    chat_room_id = href[href.find('%')+3:href.find('&')]
            else:
                chat_room_id = href[href.find('cid.g.')+6:href.find('&')]
            unread_chat_room_id.append(chat_room_id)
        
        return unread_chat_room_id

    def send_msg(self, chat_room_id, content):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = 'https://m.facebook.com/messages/send/'
        if len(str(chat_room_id)) > len(self.user_id):
            self.send_msg_data['tids'] = 'cid.g.%s'%str(chat_room_id)
        else:
            self.send_msg_data['tids'] = '%s'%str(chat_room_id)
            self.send_msg_data['ids[%s]'%str(chat_room_id)] = str(chat_room_id)
        self.send_msg_data['body'] = content
        self.session.post(url, data=self.send_msg_data)