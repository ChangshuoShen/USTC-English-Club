from django.db import models
from django.utils import timezone
# Create your models here.
class riddles(models.Model):
    riddle_id = models.CharField(verbose_name = 'riddle_id', maxlength = 20, blank = False)
    main_category = models.CharField(verbose_name = 'main_category', max_length = 64, blank = False)
    riddles_text = models.CharField(verbose_name = 'riddles_text', max_length = 512, blank = False)
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