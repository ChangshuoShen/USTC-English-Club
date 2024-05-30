from django.shortcuts import render, HttpResponse
from .models import post

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
    print(contents)
    all_contents = []
    
    for i in range(1, 5+1):
        all_contents.append((i, ['contents'] * 3))
    return render(request, 'forum_index.html', {
        'all_contents': all_contents,
    })


def share(request):
    return render(request, 'share.html')



def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['imageFile']  # 'myfile' 是文件 input 元素的 name 属性值
        print(uploaded_file)
        print(uploaded_file.name)  # 打印文件名
        print(uploaded_file.size)  # 打印文件大小
        print(uploaded_file.content_type)  # 打印文件类型
    else:
        # 处理 GET 请求的逻辑
        pass


def submit_sharing(request):
    if request.method == 'POST':
        print('request.POST.get', request.POST.get)
        upload_file(request)
        return HttpResponse(request.POST.get('content_copy'))
    else:
        return HttpResponse('Submitted')


def show_post_detail(request):
    # return HttpResponse('Show More Information Here')
    main_comments = []
    for i in range(2):
        main_comments.append(
            {
                'main': 'mainmainmain',
                'id': i,
                'replys': ["123"] * 3,
            }
        )

    return render(request, 'post_details.html', {
        'main_comments': main_comments,
    })


def user_question(request):
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

