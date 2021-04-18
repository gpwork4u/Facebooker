import re
import json
from bs4 import BeautifulSoup
from .data_type import PostInfo


def letter_adder(string: str, num: int):
    if ord(string[1]) + num % 26 >= ord('z'):
        string = chr(ord(string[0])+1) + chr(ord(string[1]) + num - 26)
    else:
        string = string[0] + chr(ord(string[1]) + num)
    return string


def get_login_data(html_text):
    soup = BeautifulSoup(html_text, 'lxml')
    hiiden_input_data = soup.find('form').findAll(
        'input', {'type': 'hidden'})
    data = {}
    for input_data in hiiden_input_data:
        data[input_data.get('name')] = input_data.get('value')
    return data


def get_fb_dtsg(html_text):
    soup = BeautifulSoup(html_text, 'lxml')
    fb_dtsg = soup.find('input', {'name': 'fb_dtsg'})
    if not fb_dtsg:
        return ''
    return fb_dtsg.get('value')


def post_parser(html_text, post_id, url):
    soup = BeautifulSoup(html_text, 'lxml')
    post_content = soup.find('div', id='m_story_permalink_view')
    if not post_content:
        return None
    author = post_content.find('h3', recursive=True).text
    content = str(post_content.find('div', {'data-ft': '{"tn":"*s"}'}))
    content = content.replace('<br/> ', '\n')
    content = content.replace('<br/>', '\n')
    content = re.sub('<[^>]+> ', '', content)
    content = re.sub('<[^>]+>', '', content)
    time = post_content.find('footer').find('abbr').text
    post_image = post_content.find('div', {'data-ft': '{"tn":"H"}'})
    images = []
    link = None
    if post_image:
        for img_src in post_image.find_all('img', class_='s'):
            src = img_src.get('src')
            images.append(src)
        link = post_image.find('a')
        if link:
            link = link.get('href')
    post_info = PostInfo(post_id,
                         url,
                         author,
                         content,
                         time,
                         images,
                         link)
    return post_info


def get_like_action_href(html_text):
    soup = BeautifulSoup(req.text, 'lxml')
    root = soup.find('div', id='root').find(
        'table', role='presentation')
    action_href = [a.get('href') for a in root.findAll('a')][:-1]
    return action_href


def post_list_parser(soup):
    posts = soup.find('section').findAll('article', recursive=False)
    for post in posts:
        data = json.loads(post.get('data-ft'))
        if 'mf_story_key' not in data:
            continue
        post_id = data['mf_story_key']
        yield post_id
