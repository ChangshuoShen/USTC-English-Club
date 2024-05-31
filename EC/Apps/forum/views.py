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
    contents = post.get_posts_by_theme()
    # print(contents)

    return render(request, 'forum_index.html', {
        'contents': contents.items(),
        })


def share(request):
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
        # upload_file(request)
        return HttpResponse(request.POST.get('content_copy'))
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

