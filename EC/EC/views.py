from django.shortcuts import render, redirect, HttpResponse
from Apps.accounts.models import User

def index(request):
    # # 检查用户的 cookie
    # user_id = request.COOKIES.get('user_id')
    # email = request.COOKIES.get('email')
    # print(request.COOKIES)
    # # 如果存在用户信息的 cookie，将用户视为已登录
    # if user_id and email:
    #     # 进一步检查用户是否存在于数据库中
    #     try:
    #         user = User.get_user_by_email(email)
    #         if user and user.id == int(user_id):
    #             request.session['user_id'] = user.id
    #             request.session['email'] = user.email
    #             print('yes')
    #             return render(request, 'index.html')
    #         else:
    #             # 清除无效的用户信息 cookie 并重定向到登录页面
    #             response = redirect('accounts:signup_login')
    #             response.delete_cookie('user_id')
    #             response.delete_cookie('email')
    #             return response
    #     except Exception as e:
    #         # 其他异常情况，重定向到登录页面
    #         return redirect('accounts:signup_login')
    # else:
    return render(request, 'index.html')