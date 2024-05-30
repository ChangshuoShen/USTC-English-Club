from .models import post

def add_post():
    '''
    这里为每个主题添加三个post，让GPT写
    '''
    themes = post.create_post(4, 'guess', "What's My Name")