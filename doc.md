# Facebooker Guide

## How to use
```python
from Facebooker import facebook
fb = facebook.API.login(email, password)
```
## Data Type

### comments_info
- comments_info.id : the comment's id
- comments_info.author : the comment send from
- comments_info.content : content of the comment
- comments_info.time : the comment send time

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
facebook.API.get_post(post_id, group_id=None)
```
> get target post
- input:
  - post_id : target post id
  - group_id : the group of the target post, if target post is not in a group set None.
- return:
  - a html format of the post 
  
### like_post
```python
  facebook.API.like_post(action, post_id)
```
- inputs
  - action : an 0 ~ 6 number
    - 0 : like
    - 1 : Love
    - 2 : Care
    - 3 : Haha
    - 4 : Wow
    - 5 : Sad
    - 6 : Angry
  - post_id : target post id

### get_user_post_list
```python
facebook.API.get_user_post_list(user_id, num=10)
```
> get posts on target user's wall
- input
  - user_id : target user id
  - num : the number of posts

- return
  - all posts id on user's wall
### get_group_post_list
```python
facebook.API.get_group_post_list(group_id, num=10)
```
> get posts on target user's wall
- input
  - group_id : target user id
  - num : the number of posts

- return
  - the number posts id in group

### get_fanpage_post_list
```python
facebook.API.get_group_post_list(fanpage_id, num=10)
```
> get posts on target user's wall
- input
  - group_id : target user id
  - num : the number of posts

- return
  - the number posts id in group
### post
```python
facebook.API.post(content, privacy_level=facebook.data_type.privacy_level.PUBLIC)
```
> post a post
- input
  - content : the post content
  - privacy_level: facebook.data_type.privacy_level.PUBLIC for public
                   facebook.data_type.privacy_level.FRIENDS for friend
                   

### post_to_target
```python
facebook.API.post_to_target(self, content, target_id=None, target_type=None)
```
> post a post to target's wall
- input
  - content : the post content
  - target_id : the target's id ,it can be user, group or fanpage
  - target_type : the target's type
    - 0 : user
    - 1 : group
    - 2 : fanpage

### fanpage_post
```python
facebook.API.fanpage_post(self, content, fanpage_id)
```
> post a fanpage post
- input
  - content : the post content
  - fanpage_id : the fanpage's id of the post 
  
### get_comments
```python
facebook.API.get_comments(post_id, num=10, start=0)
```
> get all comments under the post

- input:
  - post_id : target post id
  - num : the number of commnents you want
  - start : the last comment you want to start
- return 
  - a list of comment_info

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
facebook.API.get_msg(chat_room_id ,num=1)
```
> get messages from target char room

- input:
  - chat_room_id : target user id or group id
  - num : the number of message you want to get
- return 
  - a list of tuple start with the latest message:
    - the user who send the message
    - the message content
    - the message time

### get_unread_chat
```
facebook.API.get_msg()
```
> get chat room id that you have not read

- return
  - a list of chat room id that have not unread message
   