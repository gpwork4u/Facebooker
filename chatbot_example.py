import time
from Facebooker import facebook
import sys
from getpass import getpass
fb = facebook.API()
email = input('email:')
password = getpass('password:')
fb.login(email, password)
while True:
    unread_chats = fb.get_unread_chat()
    for chat in unread_chats:
        msg = fb.get_msg(chat)[1][-1]
        print('get chat id:%s, message:%s'%(chat, msg))
        if msg == 'test':
            fb.send_msg(chat, 'test')
        else:
            fb.send_msg(chat, 'this is fb bot')
    time.sleep(0.01)