# Facebooker Guide

## login
> login to facebook
- input:
  - email
  - password

it will save cookie if cookie is not found, or you have cooki file it will login by the cookie not email and password

## post

### get_post
> get target post
- input:
  - post_id : target post id
- return:
  - a html format of the post 
  

### post
> post a post to your or friend's wall
- input
  - content : the post content you want
  - privacy_level: privacy level of your post, 0 for public, 1 for freind, if target isn't None, it will not effect
  - target : target user id, leave None if you want to post on your wall

### get_user_post_list
> get posts on target user's wall
- input
  - user_id : target user id

- return
  - all posts id on user's wall

## comment

### get_comments

> get all comments under the post

- input:
  - post_id : target post id

- return 
  - all comments under the post with 

### delete_comment
> delete target comment
- input
    - comment_id : target comment id
    - post_id : the post of target comment

### comment
> comment to post
- input
    - post_id : target post id


## reply
### reply
> reply a comment
- input
  - post_id : the post id of target comment 
  - comment_id : target comment id
## messenger

### send_msg
> send a message to a user or a group

- input
  - chat_room_id : target user id or group id
  - content : message content

### get_msg
> get messages from target char room

- input:
  - chat_room_id : target user id or group id
  
  - return:
    - the newest messages in target chat room
   