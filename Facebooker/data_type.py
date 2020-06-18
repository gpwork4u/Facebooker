class comment_info:
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