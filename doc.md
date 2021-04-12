# Facebooker Guide

## How to use
```python
from Facebooker import facebook
fb = facebook.API()
fb.login(email, password)
```
## Data Type

### PostInfo
- PostInfo.id : the post's id
- PostInfo.author : the post send from
- PostInfo.content : post of the comment
- PostInfo.time : the post send time
- PostInfo.images : images in the post, stored in a numpy array with BGR color channel
- PostInfo.link : link in the post, if there are no link it will be None
### CommentInfo
- CommentInfo.id : the comment's id
- CommentInfo.author : the comment send from
- CommentInfo.content : content of the comment
- CommentInfo.time : the comment send time

## Option
### privacy_level
- facebook.privacy_level.PUBLIC : post for public
- facebook.privacy_level.FRIENDS : post for friends

### like_action
- facebook.like_action.LIKE
- facebook.like_action.LOVE
- facebook.like_action.CARE
- facebook.like_action.HAHA
- facebook.like_action.WOW
- facebook.like_action.SAD
- facebook.like_action.ANGRY

## API functions
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
  - a PostInfo object 
  
### like_post
```python
  facebook.API.like_post(post_id, action=facebook.data_type.like_action.LIKE)
```
- inputs
  - post_id : target post id
  - action : [like_action](#like_action)


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
  - privacy_level : [privacy_level](#privacy_level)
                   

### post_to_target
```python
facebook.API.post_to_target(content, target_id=None, target_type=None)
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
facebook.API.fanpage_post(content, fanpage_id)
```
> post a fanpage post
- input
  - content : the post content
  - fanpage_id : the fanpage's id of the post 
  
### fanpage_post_photo
```
facebook.API.fanpage_post_photo(text_content, image, fanpage_id)
```
> post a fanpage post with an image

- input
  - text_content : the post content text
  - image : the post image which type is _io.BufferedReader
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
  - a list of [comment_info](#comments_info) object

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

### send_image_msg
```python
facebook.API.send_image_msg(chat_room_id, image, content)
```
> send a message to a user or a group

- input
  - chat_room_id : target user id or group id
  - image : the post image which type is _io.BufferedReader
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
   