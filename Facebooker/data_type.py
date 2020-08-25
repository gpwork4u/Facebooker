class PostInfo:
    def __init__(self,
                 post_id:str,
                 author:str,
                 content:str,
                 time:str
                 ):
        self.id = post_id
        self.author = author
        self.content = content
        self.time = time

class CommentInfo:
    def __init__(self,
                 comment_id:str,
                 author:str,
                 content:str,
                 time:str,
                 ):
        self.id = comment_id
        self.author = author
        self.content = content
        self.time = time