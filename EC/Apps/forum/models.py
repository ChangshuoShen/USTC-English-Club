from django.db import models
from django.utils import timezone
from Apps.accounts.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from django.db import transaction # 做一些事务锁
# Create your models here.

class post(models.Model):
    class ThemeChoices(models.TextChoices):
        '''
        这里是五类post
        '''
        
        THEME_ONE = 'Riddle', 'Riddle'
        THEME_TWO = 'Share Something Interesting', 'Share Something Interesting'
        THEME_THREE = 'Ask For Help', 'Ask For Help'
        THEME_FOUR = 'Find Friends', 'Find Friends'
        THEME_FIVE = 'Else', 'Else'
    # post_id = models.CharField(verbose_name='post_id', max_length = 20, blank = False)
    
    publisher_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.TextField(verbose_name='title', blank = False)
    post_content = models.TextField(verbose_name='post_content', blank = False)
    
    theme = models.CharField(
        verbose_name='theme',
        max_length=50,
        choices=ThemeChoices.choices,
        default=ThemeChoices.THEME_FIVE,
        blank=False
    )
    
    publish_date = models.DateTimeField(verbose_name='published_date', default=timezone.now)
    post_likes = models.IntegerField(default=0, verbose_name='likes')

    # main_category = models.CharField(max_length=100, blank=True, null=True)
    # answer_text = models.TextField(blank=True, null=True)
    # difficulty = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        # if self.theme == self.ThemeChoices.THEME_ONE:
        #     # 主题为 "Riddle" 时，这些字段是必需的
        #     if not (self.main_category and self.answer_text and self.difficulty):
        #         raise ValueError("For Riddle posts, main_category, answer_text, and difficulty are required.")
        # else:
            # self.main_category = None
            # self.answer_text = None
            # self.difficulty = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.post_title
    
    @classmethod
    def create_post(cls, publisher_id, post_title, post_content, theme):
        post_object = cls.objects.create(
            publisher_id=publisher_id,
            post_title=post_title,
            post_content=post_content,
            theme=theme
        )
        return post_object

    @classmethod
    def get_post_by_id(cls, post_id):
        try:
            post_object = get_object_or_404(cls, id=post_id)
            return {
                'id': post_object.id,
                'publisher_id': post_object.publisher_id.id,  # Assuming you want the ID of the publisher
                'post_title': post_object.post_title,
                'post_detail': post_object.post_content,  # post_content key renamed to post_detail
                'theme': post_object.theme,
                'publish_date': post_object.publish_date,
                'post_likes': post_object.post_likes
            }
        except Http404:
            return None

    @classmethod
    def get_post_instance_by_id(cls, post_id):
        return get_object_or_404(cls, id=post_id)
    
    @classmethod
    def get_all_posts(cls):
        return cls.objects.all()
    
    
    @classmethod
    def update_post(cls, post_id, post_title=None, post_content=None, theme=None):
        post_object = get_object_or_404(cls, id=post_id)
        if post_title:
            post_object.post_title = post_title
        if post_content:
            post_object.post_content = post_content
        if theme:
            post_object.theme = theme
        post_object.save()
        return post_object

    @classmethod
    def delete_post(cls, post_id):
        post_object = get_object_or_404(cls, id=post_id)
        post_object.delete()
        
        
    @classmethod
    def get_posts_by_theme(cls, page, items_per_page = 10):
        """
        获取所有帖子，并按照主题分类，支持分页
        """
        # 创建一个空字典用于存储帖子按主题分类
        posts_by_theme = {}
        paginated_posts_by_theme = {}

        # 遍历所有主题选项
        for i, theme_choice in enumerate(cls.ThemeChoices.choices, start=1):
            theme_name = theme_choice[0]  # 主题名称
            theme_posts = cls.objects.filter(theme=theme_name).order_by('-publish_date')
            paginator = Paginator(theme_posts, items_per_page)
            # 获取对应页的数据
            page_obj = paginator.get_page(page)

            posts_by_theme[i] = [
                {
                    'id': post.id,
                    'publisher_id': post.publisher_id.id,
                    'post_title': post.post_title,
                    'post_detail': post.post_content,
                    'theme': post.theme,
                    'publish_date': post.publish_date,
                    'post_likes': post.post_likes
                }
                for post in page_obj
            ]

            paginated_posts_by_theme[i] = {
                'posts': posts_by_theme[i],
                'paginator': paginator,
                'page_obj': page_obj
            }

        return paginated_posts_by_theme

    @classmethod
    def get_riddles_by_difficulty(cls):
        riddles_by_difficulty = {}
        difficulties = ['Easy', 'Medium', 'Hard']

        for difficulty in difficulties:
            riddle_posts = cls.objects.filter(theme=cls.ThemeChoices.THEME_ONE, difficulty=difficulty)

            riddles_by_difficulty[difficulty] = [
                {
                    'id': post.id,
                    'publisher_id': post.publisher_id.id,
                    'post_title': post.post_title,
                    'post_detail': post.post_content,
                    'theme': post.theme,
                    'publish_date': post.publish_date,
                    'post_likes': post.post_likes,
                    'main_category': post.main_category,
                    'answer_text': post.answer_text,
                    'difficulty': post.difficulty
                }
                for post in riddle_posts
            ]

        return riddles_by_difficulty
    
    @classmethod
    def get_riddles_by_main_category(cls):
        """
        获取所有Riddle帖子，并按照主题（main_category）分类
        """
        # 创建一个空字典用于存储帖子按主题分类
        riddles_by_category = {}

        # 首先筛选出所有的Riddle帖子
        riddles = cls.objects.filter(theme=cls.ThemeChoices.THEME_ONE)

        # 遍历所有筛选出的Riddle帖子
        for riddle in riddles:
            category = riddle.main_category  # 获取帖子的主题分类
            if category not in riddles_by_category:
                riddles_by_category[category] = []

        # 将每个Riddle的详细信息存储在字典中
            riddles_by_category[category].append({
                'id': riddle.id,
                'publisher_id': riddle.publisher_id.id,
                'post_title': riddle.post_title,
                'post_detail': riddle.post_content,
                'theme': riddle.theme,
                'publish_date': riddle.publish_date,
                'post_likes': riddle.post_likes,
                'main_category': riddle.main_category,
                'answer_text': riddle.answer_text,
                'difficulty': riddle.difficulty
            })

        return riddles_by_category


class Comment(models.Model):
    post = models.ForeignKey(post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content = models.TextField(verbose_name='comment_content', blank=False)
    comment_date = models.DateTimeField(verbose_name='created_at', default=timezone.now)
    comment_likes = models.IntegerField(default=0, verbose_name='likes')

    def __str__(self):
        return f'Comment by {self.user.name} on {self.post.post_title}'

    @classmethod
    def find_comments_on_specific_post(cls, post):
        return cls.objects.filter(post=post)

    @classmethod
    def find_comments_on_specific_post_through_post_id(cls, post_id):
        return cls.objects.filter(post=post_id).order_by('-comment_date')
    
    @classmethod
    def create_comment(cls, post, user, content):
        comment = cls.objects.create(post=post, user=user, content=content)
        return comment

    @classmethod
    def delete_comment(cls, comment_id):
        comment = cls.objects.get(id=comment_id)
        comment.delete()

    @classmethod
    def update_comment(cls, comment_id, content):
        comment = cls.objects.get(id=comment_id)
        comment.content = content
        comment.save()

    @classmethod
    def get_comment_by_id(cls, comment_id):
        return cls.objects.get(id=comment_id)

class Reply(models.Model):
    '''
    专指针对某个评论的reply
    '''
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    reply_content = models.TextField(verbose_name='reply_content', blank=False)
    reply_date = models.DateTimeField(verbose_name='created_at', default=timezone.now)

    def __str__(self):
        return f'Reply by {self.user.name}'

    @classmethod
    def find_replies_on_specific_comment_through_comment_id(cls, comment_id):
        return cls.objects.filter(comment=comment_id).order_by('-reply_date')
    
    @classmethod
    def create_reply(cls, comment, user, content):
        reply = cls.objects.create(comment=comment, user=user, reply_content=content)
        return reply

    @classmethod
    def delete_reply(cls, reply_id):
        reply = cls.objects.get(id=reply_id)
        reply.delete()

    @classmethod
    def update_reply(cls, reply_id, content):
        reply = cls.objects.get(id=reply_id)
        reply.reply_content = content
        reply.save()

    @classmethod
    def get_reply_by_id(cls, reply_id):
        return cls.objects.get(id=reply_id)

class Like(models.Model):
    '''
    这里记录点赞关系
    '''
    post = models.ForeignKey(post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='created_at', default=timezone.now)

    def __str__(self):
        return f'Like by {self.user.name} on {self.post.post_title}'
    
    @classmethod
    def like_post(cls, post_instance, user_instance):
        '''
        注意传入的两个参数都是实例
        '''
        if not cls.objects.filter(post=post_instance, user=user_instance).exists():
            new_like = cls.objects.create(post=post_instance, user=user_instance)
            # 这一行相当于是trigger了
            # post_instance.likes = cls.count_likes_for_post(post_id=post_instance)
            post_instance.likes += 1
            new_like.save()
            post_instance.save()

    @classmethod
    def unlike_post(cls, post_instance, user_instance):
        like_queryset = cls.objects.filter(post=post_instance, user=user_instance)
        if like_queryset.exists():
            like_queryset.delete()
            # post_instance.likes = cls.count_likes_for_post(post_id=post_instance)
            post_instance.likes -= 1
            post_instance.save()

    @classmethod
    def count_likes_for_post(cls, post_id):
        # 暂时用处不大，但是后面可能会用到 
        return cls.objects.filter(post_id=post_id).count()

    @classmethod
    def count_likes_by_user(cls, user_id):
        return cls.objects.filter(user_id=user_id).count()





'''
# 下面这部分课程中先不用了
# class CommentLike(models.Model):
#     liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
#     like_time = models.DateTimeField(default=timezone.now)
#     liked_comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')

#     def __str__(self):
#         return f"{self.liker.name} liked {self.liked_comment_id}"

#     @classmethod
#     def like_comment(cls, user, comment):
#         if not cls.objects.filter(liker=user, liked_comment=comment).exists():
#             cls.objects.create(liker=user, liked_comment=comment)
#             comment.likes += 1
#             comment.save()

#     @classmethod
#     def unlike_comment(cls, user, comment):
#         if cls.objects.filter(liker=user, liked_comment=comment).exists():
#             cls.objects.filter(liker=user, liked_comment=comment).delete()
#             comment.likes -= 1
#             comment.save()
    
#     @classmethod
#     def count_likes_for_comment(cls, comment_id):
#         return cls.objects.filter(id=comment_id).values_list('comment_likes', flat=True).first()

#     @classmethod
#     def count_likes_by_user(cls, user_id):
#         return cls.objects.filter(user_id=user_id).aggregate(sum('comment_likes'))['comment_likes__sum']



# class riddles(models.Model):
#     riddle_id = models.CharField(verbose_name = 'riddle_id', max_length = 20, blank = False)
#     main_category = models.CharField(verbose_name = 'main_category', max_length = 64, blank = False)
#     riddles_text = models.TextField(verbose_name = 'riddles_text', blank = False)
#     # riddles_text = models.TextField(_(""))
#     answer_text =  models.CharField(verbose_name = 'answer_text', max_length = 512, blank = False)
#     writein_date = models.DateTimeField(verbose_name='writein_date', default=timezone.now)

#     @classmethod
#     def create_riddles(cls, name='offical_riddles', main_category=None, riddles_text=None, answer_text=None, writein_date=None):
#         """
#         创建riddles
#         """
#         riddles = cls(
#             main_category = main_category,
#             riddles_text = riddles_text,
#             answer_text = answer_text,
#             writein_date = timezone.now()
#         )

#         riddles.save()
#         return riddles
'''