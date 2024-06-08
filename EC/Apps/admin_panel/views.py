from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.utils import timezone
from Apps.accounts.models import User
from Apps.forum.models import post, Comment, Like
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

THEME_ONE = 'Riddle', 'Riddle'
THEME_TWO = 'Share Something Interesting', 'Share Something Interesting'
THEME_THREE = 'Ask For Help', 'Ask For Help'
THEME_FOUR = 'Find Friends', 'Find Friends'
THEME_FIVE = 'Else', 'Else'

def dashboard(request):
    # 获取统计数据
    total_accounts, accounts_today, accounts_yesterday = User.get_user_counts()
    total_posts, posts_today, posts_yesterday = post.get_post_counts()
    total_comments, comments_today, comments_yesterday = Comment.get_comment_counts()

    # 获取最新的帖子和用户
    latest_posts = post.get_latest_posts()
    latest_comments = Comment.get_latest_comments()

    context = {
        'total_accounts': total_accounts,
        'accounts_today': accounts_today,
        'accounts_yesterday': accounts_yesterday,
        
        'total_posts': total_posts,
        'posts_today': posts_today,
        'posts_yesterday': posts_yesterday,
        
        'total_comments': total_comments,
        'comments_today': comments_today,
        'comments_yesterday': comments_yesterday,
        
        'latest_posts': latest_posts,
        'latest_comments': latest_comments,
    }

    return render(request, 'dashboard.html', context)

def post_list(request):
    return render(request, 'post-list.html')


def riddles(request):
    riddles_list = post.get_posts_for_single_theme('Riddle')
    paginator = Paginator(riddles_list, 20)  # 每页显示20条帖子
    page_number = request.GET.get('page')
    try:
        riddles_page = paginator.page(page_number)
    except PageNotAnInteger:
        riddles_page = paginator.page(1)  # 如果page参数不是整数，则显示第一页
    except EmptyPage:
        riddles_page = paginator.page(paginator.num_pages)  # 如果page参数超出范围，则显示最后一页

    return render(request, 'post-list.html', {
        'this_url': 'admin_panel:riddles',
        'posts': riddles_page,
    })


def share_sth_interesting(request):
    interest_list = post.get_posts_for_single_theme('Share Something Interesting')
    paginator = Paginator(interest_list, 20)
    page_number = request.GET.get('page')
    try:
        interest_page = paginator.page(page_number)
    except PageNotAnInteger:
        interest_page = paginator.page(1)
    except EmptyPage:
        interest_page = paginator.page(paginator.num_pages)

    return render(request, 'post-list.html', {
        'posts': interest_page,
        'this_url': 'admin_panel:share_sth_interesting',
    })

def find_friends(request):
    friends_list = post.get_posts_for_single_theme('Find Friends')
    paginator = Paginator(friends_list, 20)
    page_number = request.GET.get('page')
    try:
        friends_page = paginator.page(page_number)
    except PageNotAnInteger:
        friends_page = paginator.page(1)
    except EmptyPage:
        friends_page = paginator.page(paginator.num_pages)

    return render(request, 'post-list.html', {
        'posts': friends_page,
        'this_url': 'admin_panel:find_friends',
    })

def ask_for_help(request):
    aid_list = post.get_posts_for_single_theme('Ask For Help')
    paginator = Paginator(aid_list, 20)
    page_number = request.GET.get('page')
    try:
        aid_page = paginator.page(page_number)
    except PageNotAnInteger:
        aid_page = paginator.page(1)
    except EmptyPage:
        aid_page = paginator.page(paginator.num_pages)

    return render(request, 'post-list.html', {
        'posts': aid_page,
        'this_url': 'admin_panel:ask_for_help',
    })

def else_list(request):
    else_list = post.get_posts_for_single_theme('Else')
    paginator = Paginator(else_list, 20)
    page_number = request.GET.get('page')
    try:
        else_page = paginator.page(page_number)
    except PageNotAnInteger:
        else_page = paginator.page(1)
    except EmptyPage:
        else_page = paginator.page(paginator.num_pages)

    return render(request, 'post-list.html', {
        'posts': else_page,
        'this_url': 'admin_panel:else',
    })


def delete_post(request):
    if request.method == "POST":
        post_id = int(request.POST.get('post_id'))
        return_url = request.POST.get('return_url')
        print('\n\n\n\n\n\n\n\n\n\n\n')
        print(post_id, return_url)
        print('\n\n\n\n\n\n\n\n\n\n\n')
        post.delete_post(post_id=post_id)
        return redirect(reverse(return_url))
        
    return HttpResponse('hello')