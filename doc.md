# Facebooker Guide

## How to use
```python
from Facebooker import facebook
fb = facebook.API.login(email, password)
```

## API member functions
### login
```python
facebook.API.login(email, password)
```
> login to facebook
- input:
  - email
  - password

it will save cookie when first time login, or you have cookie file it will login by the cookie not email and password


### get_post
```python
facebook.API.get_post(post_id)
```
> get target post
- input:
  - post_id : target post id
- return:
  - a html format of the post 
  

### post
```python
facebook.API.post(content, privacy_level, user_id)
```
> post a post to your or friend's wall
- input
  - content : the post content you want
  - privacy_level: privacy level of your post, 0 for public, 1 for freind, if user_id isn't None, it will not effect
  - user_id : target user id, leave None if you want to post on your wall

### get_user_post_list
```python
facebook.API.post(user_id)
```
> get posts on target user's wall
- input
  - user_id : target user id

- return
  - all posts id on user's wall


### get_comments
```python
facebook.API.get_comments(post_id)
```
> get all comments under the post

- input:
  - post_id : target post id

- return 
  - all comments under the post with 

### delete_comment
```python
facebook.API.delete_comment(comment_id, post_id)
```
> delete target comment
- input
    - comment_id : target comment id
    - post_id : the post of target comment

### comment
```python
facebook.API.comment(post_id, content)
```
> comment to post
- input
    - post_id : target post id
    - content : your comment content



### reply
```python
facebook.API.reply(post_id, comment_id, content)
```
> reply a comment
- input
  - post_id : the post id of target comment 
  - comment_id : target comment id

### send_msg
```python
facebook.API.send_msg(chat_room_id, content)
```
> send a message to a user or a group

- input
  - chat_room_id : target user id or group id
  - content : message content

### get_msg
```python
facebook.API.get_msg(chat_room_id)
```
> get messages from target char room

- input:
  - chat_room_id : target user id or group id
  
- return:
  - the newest messages in target chat room

### get_unread_chat
facebook.API.get_msg()

> get chat room id that you have not read

- return
  - a list chat room id have not read
   