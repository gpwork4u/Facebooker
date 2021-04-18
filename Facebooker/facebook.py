from Facebooker.parsers import post_parser
import requests
import pickle
import os
import logging
import time
import json
import re
from requests_toolbelt import MultipartEncoder
from bs4 import BeautifulSoup
try:
    import data_type
    import privacy_level
    import like_action
    import urls
    import parsers
    from constants import HEADERS, SEND_MSG_FORM_DATA, POST_FORM_DATA
except ModuleNotFoundError:
    from . import data_type
    from . import privacy_level
    from . import like_action
    from . import urls
    from . import parsers
    from .constants import HEADERS, SEND_MSG_FORM_DATA, POST_FORM_DATA


class API:
    '''
    FB post structure:
        post
        |
        --comment
            |
            --reply
    '''
    post_form_data = POST_FORM_DATA
    send_msg_form_data = SEND_MSG_FORM_DATA
    login_check = False

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(HEADERS)

    def login(self, email: str, password: str):
        # get input field
        self.session.cookies.clear()
        if os.path.isfile(email+'.cookie'):
            self._load_cookies(email+'.cookie')
        req = self.session.get(urls.M_FACEBOOK)
        self.fb_dtsg = parsers.get_fb_dtsg(req.text)
        if not self.fb_dtsg:
            login_url = urls.join(urls.M_FACEBOOK, 'login')
            req = self.session.get(login_url)
            data = parsers.get_login_data(req.text)
            # input email and password
            data['email'] = email
            data['pass'] = password
            # login
            req = self.session.post(login_url, data=data)
        cookies = self.session.cookies.get_dict()
        if 'c_user' not in cookies:
            return False
        self.user_id = cookies['c_user']
        req = self.session.get(urls.M_FACEBOOK)
        self.fb_dtsg = parsers.get_fb_dtsg(req.text)
        self.login_check = True
        self._save_cookies(email+'.cookie')
        self.send_msg_form_data['fb_dtsg'] = self.fb_dtsg,
        self.post_form_data['fb_dtsg'] = self.fb_dtsg
        self.post_form_data['target'] = self.user_id
        return True

    def _save_cookies(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(self.session.cookies, f)

    def _load_cookies(self, filename: str):
        with open(filename, 'rb') as f:
            self.session.cookies.update(pickle.load(f))

    # post methods
    def get_post(self, post_id: str, group_id=None):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = urls.join(urls.MBASIC_FACEBOOK,
                        'story.php?story_fbid=%s&id=1' % str(post_id))
        if group_id:
            url = urls.join(urls.MBASIC_FACEBOOK,
                            'groups/%s?' % str(group_id),
                            'view=permalink&id=%s' % str(post_id))
        req = self.session.get(url)
        post_info = post_parser(req.text, post_id, url)

        if not post_info:
            logging.error(
                'This post is not supported or you don\'t have acess authority')
        return post_info

    def like_post(self, post_id, action=like_action.LIKE):
        if not self.login_check:
            logging.error('You should login first')
            return
        if action > 6 or action < 0:
            logging.error('This action is not supported')
            return
        url = urls.join(urls.MBASIC_FACEBOOK,
                        '/reactions/picker/?ft_id='+str(post_id))
        req = self.session.get(url)
        try:
            action_href = parsers.get_like_action_href(req.text)
            like_url = urls.MBASIC_FACEBOOK + action_href[action]
            self.session.get(like_url)
        except Exception:
            logging.error('You don\'t have access authority')

    def get_user_post_list(self, user_id):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = urls.join(urls.M_FACEBOOK, '%s?tsid=1' % str(user_id))
        while True:
            req = self.session.get(url)
            soup = BeautifulSoup(req.text, 'lxml')
            post_ids = parsers.post_list_parser(soup)
            for post_id in post_ids:
                yield post_id
            next_page_div = soup.find('section').next_sibling
            if next_page_div.get('id'):
                next_href = next_page_div.find('a').get('href')
                url = urls.M_FACEBOOK + next_href
            else:
                break

    def get_group_post_list(self, group_id):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = urls.join(urls.M_FACEBOOK, '/groups/%s' % str(group_id))
        while True:
            req = self.session.get(url)
            soup = BeautifulSoup(req.text, 'lxml')
            soup = soup.find('div', id='m_group_stories_container')
            post_ids = parsers.post_list_parser(soup)
            for post_id in post_ids:
                yield post_id
            next_page_link = soup.find('section').next_sibling.find('a')
            if next_page_link:
                next_href = next_page_link.get('href')
                url = urls.join(urls.MBASIC_FACEBOOK, next_href)
            else:
                break

    def get_fanpage_post_list(self, fanpage_id):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = urls.join(urls.M_FACEBOOK,
                        f'page_content_list_view/more/?' +
                        f'page_id={fanpage_id}&start_cursor=%7B%22timeline_cursor%22%3Anull%2C%22timeline_section_cursor%22%3Anull%2C%22' +
                        f'has_next_page%22%3Atrue%7D&num_to_fetch=4&surface_type=timeline')

        while True:
            req = self.session.post(url, data={'fb_dtsg': self.fb_dtsg})
            text = req.text
            text = req.text.encode().decode("unicode-escape")
            text = text.encode('utf-16', 'surrogatepass').decode('utf-16')
            text = text.replace('\/', '/')
            soup = BeautifulSoup(text, 'lxml')
            articles = soup.findAll('article')
            for article in articles:
                if article.get('data-ft'):
                    data = json.loads(article.get('data-ft'))
                    post_id = data['mf_story_key']
                    yield post_id
            next_page_div = soup.find('div', id='see_more_cards_id')
            if not next_page_div:
                break
            next_href = next_page_div.find('a').get('href')
            url = urls.M_FACEBOOK + next_href

    def post(self,
             content,
             privacy_level=privacy_level.PUBLIC):
        if not self.login_check:
            logging.error('You should login first')
            return
        post_data = self.post_form_data
        url = urls.join(urls.MBASIC_FACEBOOK, 'composer/mbasic/')
        post_data['xc_message'] = content
        post_data['privacyx'] = privacy_level
        self.session.post(url, data=post_data)

    def post_to_target(self, content, target_id=None, target_type=None):
        ''' target_type:
                0 : user
                1 : group
                2 : fanpage
        '''
        if not self.login_check:
            logging.error('You should login first')
            return
        referrer = ['timeline', 'group', 'pages_feed']
        c_src = ['timeline_other', 'group', 'page_self']
        post_data = self.post_form_data
        url = urls.join(urls.MBASIC_FACEBOOK, '/composer/mbasic/')
        post_data['xc_message'] = content
        post_data['referrer'] = referrer[target_type]
        post_data['c_src'] = c_src[target_type]
        post_data['target'] = target_id
        post_data['id'] = target_id
        self.session.post(url, data=post_data)

    def fanpage_post(self, content, fanpage_id):
        if not self.login_check:
            logging.error('You should login first')
            return
        post_data = self.post_form_data
        url = urls.join(urls.MBASIC_FACEBOOK,
                        '/composer/mbasic/?av=%s' % str(),
                        fanpage_id)
        post_data['xc_message'] = content
        post_data['referrer'] = 'pages_feed'
        post_data['c_src'] = 'page_self'
        post_data['target'] = fanpage_id
        self.session.post(url, data=post_data)

    def fanpage_post_photo(self, text_content, image, fanpage_id):
        url = urls.join(urls.MBASIC_FACEBOOK,
                        '/composer/mbasic/',
                        '?c_src=page_self&referrer=pages_feed&',
                        'target=%s&' % fanpage_id,
                        'icv=lgc_view_photo&av=%s' % fanpage_id)
        req = self.session.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        form = soup.find('form')
        all_input_data = form.findAll('input')
        data = {}
        for input_data in all_input_data:
            data[input_data.get('name')] = input_data.get('value')

        url = urls.join(urls.MBASIC_FACEBOOK,
                        '_mupload_/composer/?av=%s' % fanpage_id)
        data['file1'] = ('image', image, 'image')
        data['xc_message'] = text_content
        m_data = MultipartEncoder(
            fields=data
        )
        self.session.post(url, data=m_data, headers={
                          'Content-Type': m_data.content_type})

    def group_sell_post(self,
                        group_id,
                        title, price,
                        location='',
                        content='',
                        images=[],
                        currency='TWD'):
        url = urls.join(urls.MBASIC_FACEBOOK, '/groups/sell/_edit/post/')
        data = {}
        data['fb_dtsg'] = self.fb_dtsg
        data['composer_attachment_sell_title'] = title
        data['composer_attachment_sell_price'] = str(price)
        data['composer_attachment_sell_pickup_note'] = location
        data['composer_attachment_sell_currency'] = currency
        data['target'] = str(group_id)
        for i, image in enumerate(images[:3]):
            data['file%d' % i] = image
        data['xc_message'] = content
        m_data = MultipartEncoder(
            fields=data
        )
        self.session.post(url, data=m_data, headers={
                          'Content-Type': m_data.content_type})
    # comment methods

    def get_comments(self, post_id, group_id=None, num=10, start=0):
        if not self.login_check:
            logging.error('You should login first')
            return

        comment_info_list = []
        while num > 0:
            url = urls.join(urls.MBASIC_FACEBOOK,
                            '/story.php?story_fbid=%s&id=1&p=%s' % (str(post_id), start))
            if group_id:
                url = urls.join(urls.MBASIC_FACEBOOK,
                                '/groups/%s?view=permalink&id=%s' % (group_id, post_id))
            req = self.session.get(url)
            soup = BeautifulSoup(req.text, 'lxml')
            try:
                div = soup.find('div', id='ufi_%s' % str(post_id))
                comment_div = div.find(
                    'div', id='sentence_%s' % str(post_id)).next_sibling
                comments = comment_div.findAll('div', recursive=False)
                if group_id and not comments:
                    comments = comment_div.next_sibling.findAll(
                        'div', recursive=False)
                comments.reverse()
            except Exception as e:
                logging.debug(e)
                logging.error('You don\'t have access authority')
                return
            for comment in comments:
                try:
                    comment_author = comment.find('h3').find('a').text
                    comment_id = comment.get('id')
                    comment_content = comment.find('h3').next_sibling.text
                    comment_time = comment.find('abbr').text
                    comment_href = comment.find('span', id='like_%s_%s' % (
                        post_id, comment_id)).next_sibling.next_sibling.get('href')
                    comment_url = urls.join(urls.MBASIC_FACEBOOK, comment_href)
                    comment_info = data_type.CommentInfo(comment_id,
                                                         comment_author,
                                                         comment_content,
                                                         comment_time,
                                                         comment_url
                                                         )
                    comment_info_list.append(comment_info)
                    num -= 1
                except Exception as e:
                    pass

            pre_page_div = comment_div.find(
                'div', id='see_prev_%s' % str(post_id))

            if pre_page_div:
                pre_href = pre_page_div.find('a').get('href')
                pre_href = pre_href[pre_href.find('p='):]
                start = pre_href[2:pre_href.find('&')]
            else:
                break

        return comment_info_list

    def delete_comment(self, post_id, comment_id):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = urls.join(urls.MBASIC_FACEBOOK,
                        '/ufi/delete/',
                        '?delete_comment_id=%s' % str(comment_id), '&delete_comment_fbid=%s' % str(comment_id), '&ft_ent_identifier=%s' % str(post_id))
        data = {'fb_dtsg': self.fb_dtsg}
        return self.session.post(url, data=data)

    def comment(self, post_id, content):
        url = urls.join(urls.MBASIC_FACEBOOK,
                        '/a/comment.php?fs=8&actionsource=2&comment_logging&ft_ent_identifier=%s' % str(post_id))
        comment = {'comment_text': content, 'fb_dtsg': self.fb_dtsg}
        return self.session.post(url, data=comment)

    # reply method
    def reply(self, post_id, comment_id, content):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = urls.join(urls.MBASIC_FACEBOOK,
                        '/a/comment.php?parent_comment_id=%s&ft_ent_identifier=%s' % (str(comment_id), str(post_id)))
        data = {'fb_dtsg': self.fb_dtsg, 'comment_text': content}
        self.session.post(url, data=data)

    def get_replies(self, post_id, comment_id, group_id=None, num=10):
        comments = self.get_comments(post_id, group_id)
        comment_id = str(comment_id)
        for comment in comments:
            print(comment.id)
            if comment.id == comment_id:
                break
        url = comment.url
        req = self.session.get(url)
        reply_info_list = []
        while num > 0:
            req = self.session.get(url)
            soup = BeautifulSoup(req.text, 'lxml')
            try:
                soup = BeautifulSoup(req.text, 'lxml')
                replies_div = soup.find('div', id=str(comment_id)).next_sibling
                replies = replies_div.findAll('div', recursive=False)
                replies.reverse()
            except Exception as e:
                logging.debug(e)
                logging.error('You don\'t have access authority')
                return
            for reply in replies:
                try:
                    reply_author = reply.find('h3').find('a').text
                    reply_id = reply.get('id')
                    reply_content = reply.find('h3').next_sibling.text
                    reply_time = reply.find('abbr').text
                    reply_info = data_type.ReplyInfo(reply_id,
                                                     reply_author,
                                                     reply_content,
                                                     reply_time,
                                                     )
                    reply_info_list.append(reply_info)
                    num -= 1
                except Exception:
                    pass
            pre_page_div = soup.find(
                'div', id='comment_replies_more_1:%s_%s' % (str(post_id), str(comment_id)))

            if pre_page_div:
                pre_href = pre_page_div.find('a').get('href')
                url = urls.join(urls.MBASIC_FACEBOOK, pre_href)
            else:
                break
        return reply_info_list

    # messenger method

    def get_msg(self, chat_room_id, num=1):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = urls.join(urls.MBASIC_FACEBOOK,
                        '/messages/read/?tid=%s' % str(chat_room_id))
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

            msgs = msg_group.findAll('div', recursive=False)[
                index].findAll('div', recursive=False)
            if msgs:
                msgs.reverse()
            for msg in msgs:
                content_class = parsers.letter_adder(msg.get('class')[-1], 1)
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
                except Exception:
                    logging.debug('Get non text message')
                    pass
            pre_page = msg_group.find('div', id='see_older')
            if not pre_page:
                break
            href = pre_page.find('a').get('href')
            url = urls.join(urls.MBASIC_FACEBOOK, href)

        return list(zip(send_from, content, time))

    def get_unread_chat(self):
        if not self.login_check:
            logging.error('You should login first')
            return
        url = urls.join(urls.MBASIC_FACEBOOK, '/messages/?folder=unread')
        req = self.session.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        unread_chats = soup.find('div', id='root').find(
            'section').findAll('table')
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
        url = urls.join(urls.MBASIC_FACEBOOK, '/messages/send/')
        if len(str(chat_room_id)) > len(self.user_id):
            self.send_msg_form_data['tids'] = 'cid.g.%s' % str(chat_room_id)
        else:
            self.send_msg_form_data['tids'] = '%s' % str(chat_room_id)
            self.send_msg_form_data['ids[%s]' %
                                    str(chat_room_id)] = str(chat_room_id)
        self.send_msg_form_data['body'] = content
        self.session.post(url, data=self.send_msg_form_data)

    def send_image_msg(self, chat_room_id, image, content):
        url = 'https://upload.facebook.com/_mupload_/mbasic/messages/attachment/photo/'
        send_data = self.send_msg_form_data.copy()
        if len(str(chat_room_id)) > len(self.user_id):
            send_data['tids'] = 'cid.g.%s' % str(chat_room_id)
        else:
            send_data['tids'] = '%s' % str(chat_room_id)
            send_data['ids[%s]' % str(chat_room_id)] = str(chat_room_id)
        send_data['tids'] = 'cid.g.%s' % str(chat_room_id)
        send_data['file1'] = ('image', image, 'image')
        send_data['body'] = content

        m_data = MultipartEncoder(
            fields=send_data
        )
        self.session.post(url, data=m_data, headers={
                          'Content-Type': m_data.content_type})
