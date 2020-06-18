class privacy_level:
    FRIENDS = 291667064279714
    PUBLIC = 300645083384735

class like_action:
    LIKE = 0
    LOVE = 1
    CARE = 2
    HAHA = 3
    WOW = 4
    SAD = 5
    ANGRY = 6

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