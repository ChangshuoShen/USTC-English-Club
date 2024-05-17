from django.shortcuts import render, HttpResponse


def forum_index(request):
    return render(request, 'forum_index.html', {
        'contents_list': [1, 2, 3, 4, 5],
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
        return HttpResponse(request.POST.get('content_copy'), request.FILES['imageFile'])
        
    return HttpResponse('Submitted')


def show_post_detail(request):
    # return HttpResponse('Show More Information Here')
    main_comments = [
        {
            'main': 'mainmainmain',
            'replys': ["123"] * 3,
        }
    ] * 3
    
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

