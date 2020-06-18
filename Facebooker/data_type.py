class privacy_level:
    FRIENDS = 291667064279714
    PUBLIC = 300645083384735

class comment_info:
    def __init__(self,
                 id:str,
                 author:str,
                 content:str,
                 time:str,
                 ):
        self.id = id
        self.author = author
        self.content = content
        self.time = time