from django.db import models
from django.utils import timezone
from accounts.models import User
# Create your models here.


class post(models.Model):
    class ThemeChoices(models.TextChoices):
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
    likes = models.IntegerField(default=0, verbose_name='likes')

    def __str__(self):
        return self.post_title
    
    def like_post(self, User):
        if not Like.objects.filter(post=self, user=User).exists():
            Like.objects.create(post=self, user=User)
            self.likes += 1
            self.save()

    def unlike_post(self, user):
        if Like.objects.filter(post=self, user=user).exists():
            Like.objects.filter(post=self, user=user).delete()
            self.likes -= 1
            self.save()

    
class Comment(models.Model):
    post = models.ForeignKey(post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='comment_content', blank=False)
    comment_time = models.DateTimeField(verbose_name='created_at', default=timezone.now)
    likes = models.IntegerField(default=0, verbose_name='likes')

    def __str__(self):
        return f'Comment by {self.user.name} on {self.post.post_title}'


class Like(models.Model):
    post = models.ForeignKey(post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='created_at', default=timezone.now)

    def __str__(self):
        return f'Like by {self.user.name} on {self.post.post_title}'



class CommentLike(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    like_time = models.DateTimeField(default=timezone.now)
    liked_comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.liker.name} liked {self.liked_comment_id}"

    @classmethod
    def like_comment(cls, user, comment):
        if not cls.objects.filter(liker=user, liked_comment=comment).exists():
            cls.objects.create(liker=user, liked_comment=comment)
            comment.likes += 1
            comment.save()

    @classmethod
    def unlike_comment(cls, user, comment):
        if cls.objects.filter(liker=user, liked_comment=comment).exists():
            cls.objects.filter(liker=user, liked_comment=comment).delete()
            comment.likes -= 1
            comment.save()



class riddles(models.Model):
    riddle_id = models.CharField(verbose_name = 'riddle_id', max_length = 20, blank = False)
    main_category = models.CharField(verbose_name = 'main_category', max_length = 64, blank = False)
    riddles_text = models.TextField(verbose_name = 'riddles_text', blank = False)
    # riddles_text = models.TextField(_(""))
    answer_text =  models.CharField(verbose_name = 'answer_text', max_length = 512, blank = False)
    writein_date = models.DateTimeField(verbose_name='writein_date', default=timezone.now)

    @classmethod
    def create_riddles(cls, name='offical_riddles', main_category=None, riddles_text=None, answer_text=None, writein_date=None):
        """
        创建riddles
        """
        riddles = cls(
            main_category = main_category,
            riddles_text = riddles_text,
            answer_text = answer_text,
            writein_date = timezone.now()
        )

        riddles.save()
        return riddles