from django.urls import path
from . import views
app_name = 'forum'


urlpatterns = [
    path('forum_index/', views.forum_index, name="forum_index"), # 这是论坛的主页
    path('share/', views.share, name="share"), # 编写帖子
    path('submit/', views.submit_sharing, name="submit_sharing"), # 实现post的提交逻辑
    path('post_detail/<int:post_id>', views.show_post_detail, name="post_detail"), # 展示一个发帖的详细信息，内容，作者的基本信息和链接，评论的图
    path('comment_or_reply/', views.comment_or_reply, name="comment_or_reply"),
    path('user_question/', views.user_question, name="user_question"), # 一个user的相关信息
    path('users/', views.users, name='users'), # 展示所有的user
]

