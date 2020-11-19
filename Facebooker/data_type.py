class PostInfo:
    def __init__(self,
                 post_id:str,
                 author:str,
                 content:str,
                 time:str,
                 images:list = [],
                 link:str = None
                 ):
        self.id = post_id
        self.author = author
        self.content = content
        self.time = time
        self.images = images
        self.link = link

class CommentInfo:
    def __init__(self,
                 comment_id:str,
                 author:str,
                 content:str,
                 time:str,
                 url:str
                 ):
        self.id = comment_id
        self.author = author
        self.content = content
        self.time = time
        self.url = url

class ReplyInfo:
    def __init__(self,
                 reply_id:str,
                 author:str,
                 content:str,
                 time:str,
                 ):
        self.id = reply_id
        self.author = author
        self.content = content
        self.time = time