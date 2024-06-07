from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib import messages
from .models import post, Comment, Reply
from Apps.accounts.models import User

def forum_index(request):
    '''
    返回的是长度为5的列表，其中再涵盖对应页的数据，对应的分别是：
    THEME_ONE = 'Riddle'
    THEME_TWO = 'Share Something Interesting'
    THEME_THREE = 'Ask For Help'
    THEME_FOUR = 'Find Friends'
    THEME_FIVE = 'Else'
    '''
    # contents = post.get_posts_by_theme()
    # print(contents)
    page = request.GET.get('page', 1)  # 获取页码
    items_per_page = 10  # 每页显示10个帖子

    # 获取按主题分类并分页后的数据，直接就是各个列都转到对应的页
    contents = post.get_posts_by_theme(page, items_per_page)

    return render(request, 'forum_index.html', {
        'contents': contents.items(),
    })



def riddle_difficulty_index(request):
    '''
    返回一个长度为3的列表，包括不同难度等级的Riddle帖子：
    0 - 'Easy'
    1 - 'Medium'
    2 - 'Hard'
    '''
    riddles_by_difficulty = post.get_riddles_by_difficulty()

    difficulties_ordered = ['easy', 'medium', 'hard']
    riddle_contents = [riddles_by_difficulty.get(difficulty, []) for difficulty in difficulties_ordered]

    return render(request, 'riddle_index.html', {
        'riddle_difficulty_contents': riddle_contents,
    })
# 我没找到你forum的index.html，只能先放在这里了，你要是看见这段代码就加上（稍加改动）

# <head>
#     <meta charset="UTF-8">
#     <title>Riddle Posts by Difficulty</title>
# </head>
# <body>
#     <h1>Riddle Posts by Difficulty</h1>
#     {% for difficulty, riddles in riddle_contents %}
#         <h2>{{ difficulty|capfirst }} Riddles</h2>
#         <ul>
#             {% for riddle in riddles %}
#                 <li>
#                     <strong>{{ riddle.post_title }}</strong> - {{ riddle.post_detail }} (Likes: {{ riddle.post_likes }})
#                 </li>
#             {% endfor %}
#         </ul>
#     {% empty %}
#         <p>No riddles available.</p>
#     {% endfor %}
# </body>

def riddle_category_index(request):
    riddles_by_category = post.get_riddles_by_main_category()
    return render(request, 'riddle_category_index.html', {
        'riddles_by_category': riddles_by_category.items(),
    })


# <head>
#     <meta charset="UTF-8">
#     <title>Riddle Posts by Category</title>
# </head>
# <body>
#     <h1>Riddle Posts by Category</h1>
#     {% for category, riddles in riddles_by_category %}
#         <h2>{{ category|capfirst }} Riddles</h2>
#         <ul>
#             {% for riddle in riddles %}
#                 <li>
#                     <strong>{{ riddle.post_title }}</strong> - {{ riddle.post_detail }} (Likes: {{ riddle.post_likes }})
#                 </li>
#             {% endfor %}
#         </ul>
#     {% empty %}
#         <p>No riddles available.</p>
#     {% endfor %}



def share(request):
    # 检查用户是否已登录
    if 'user_id' not in request.session or 'email' not in request.session:
            # 用户未登录，重定向到登录页面
            messages.error(request, 'Please log in to leave a comment or reply.')
            return redirect('accounts:signup_login')
    
    print(request.session.__dict__)
    return render(request, 'share.html')



def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['imageFile']  # 'myfile' 是文件 input 元素的 name 属性值
        print(uploaded_file)
        print(uploaded_file.name)
        print(uploaded_file.size)
        print(uploaded_file.content_type)
    else:
        # 处理 GET 请求的逻辑
        return HttpResponse("Nothing Here")


def submit_sharing(request):
    if request.method == 'POST':
        print('request.POST.get', request.POST.get)
        user_id = request.session.get('user_id')
        user = User.get_user_by_id(user_id=user_id)
        title = request.POST.get('title')
        theme = request.POST.get('theme')
        content = request.POST.get('content_copy')
        new_post = post.create_post(publisher_id=user, post_title=title, post_content=content, theme=theme)
        messages.success(request, 'post successfully')
        return show_post_detail(request=request, post_id=new_post.id)
        # upload_file(request)
        # return HttpResponse(request.POST.get('content_copy'))
    else:
        return HttpResponse('Submitted')




# from .utils.add_some_replies import create_random_replies
def show_post_detail(request, post_id):
    # create_random_replies()
    # return HttpResponse('Show More Information Here')
    post_content = post.get_post_by_id(post_id=post_id)
    
    if post_content:
        # 获取发布者的详细信息
        request.session['present_post_id'] = post_id
        publisher_id = post_content.get('publisher_id')
        user = User.get_user_by_id(publisher_id)
        publisher = {
            'id': user.id,
            'username': user.name,
            'email': user.email,
            'bio': user.bio,
            'gender': user.gender,
        }
    else:
        publisher = None
    
    # 这里开始找所有的comment
    relevant_comments = Comment.find_comments_on_specific_post_through_post_id(post_id=post_id)
    main_comments = []
    for single_comment in relevant_comments:
        # 这里查询该comment对应的所有的reply
        relevant_replies = Reply.find_replies_on_specific_comment_through_comment_id(single_comment.id)
        replies = []
        for single_reply in relevant_replies:
            # 需要传过来的有谁回复的，回复内容和回复时间
            replies.append(
                {
                    'replier': single_reply.user.name,
                    'reply_detail': single_reply.reply_content,
                    'date': single_reply.reply_date,
                }
            )
            # print(replies)
        main_comments.append(
            {
                'id': single_comment.id,
                'commenter': single_comment.user.name,
                'comment_detail': single_comment.content,
                'date': single_comment.comment_date,
                'likes': single_comment.comment_likes,
                'replies': replies,
            }
        )
    return render(request, 'post_details.html', {
        'publisher': publisher,
        'post_content': post_content,
        'main_comments': main_comments,
    })


def comment_or_reply(request):
    if request.method == 'POST':
        # 检查用户是否已登录
        print(request.session.__dict__)
        if 'user_id' not in request.session or 'email' not in request.session:
            # 用户未登录，重定向到登录页面
            messages.error(request, 'Please log in to leave a comment or reply.')
            return redirect('accounts:signup_login')
        
        
        user_id = request.session.get('user_id')
        post_id = request.session.get('present_post_id')
        # 用户已登录
        print(request.POST)
        comment_or_reply = request.POST.get('comment_or_reply')
        reply = request.POST.get('reply')
        comment_id = request.POST.get('comment_id')
        # 根据reply的值判断是评论还是回复
        
        user_instance = User.get_user_by_id(user_id=user_id)
        if reply in ('true', 'True'):
            # 这是一个回复
            comment_instance = Comment.get_comment_by_id(comment_id=comment_id)
            Reply.create_reply(comment=comment_instance, user=user_instance, content=comment_or_reply)
        else:
            # 这是一个评论
            post_instance = post.get_post_instance_by_id(post_id)
            Comment.create_comment(post=post_instance, user=user_instance, content=comment_or_reply)
        return show_post_detail(request, post_id=post_id)

    return HttpResponse("Nothing to see here")


# from .utils.add_some_comments import create_comments_for_all_users_and_posts
def user_question(request):
    # create_comments_for_all_users_and_posts()
    return render(request, 'user_question.html')


def users(request):
    num = 6
    users_info = [{'name': 'Runge',
              'rank': 'Top',
              'main_contents': '6666666666666666666666',
              }
            ] * num
    
    return render(request, 'user.html', {
        'users_info': users_info
    })

