from django.db import models

class Riddle(models.Model):
    '''
        这是一个mystery_hunt.riddle类，主要是用于放置官方的riddles，暂时主要使用的是网页上爬取的数据
    '''
    riddle_id = models.AutoField(primary_key=True)
    main_category = models.CharField(max_length=100)
    riddle_text = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)  # 新增字段，记录创建时间

    def __str__(self):
        return self.riddle_text

    @classmethod
    def create_riddle(cls, main_category, riddle_text, answer, difficulty):
        '''
            创建一个新的riddle
        '''
        return cls.objects.create(
            main_category=main_category,
            riddle_text=riddle_text,
            answer=answer,
            difficulty=difficulty
        )

    @classmethod
    def get_riddle_by_id(cls, riddle_id):
        '''
            之后跳转hunt_detail的时候需要使用id进行跳转
        '''
        try:
            return cls.objects.get(riddle_id=riddle_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_all_riddles(cls):
        return cls.objects.all()

    @classmethod
    def get_riddles_by_category(cls, category):
        return cls.objects.filter(main_category=category)

    @classmethod
    def get_riddles_by_difficulty(cls):
        from collections import defaultdict
        riddles_by_difficulty = defaultdict(list)
        riddles = cls.objects.all()
        for riddle in riddles:
            riddles_by_difficulty[riddle.difficulty].append(riddle)
        return dict(riddles_by_difficulty)
    
    
    @classmethod
    def update_riddle(cls, riddle_id, main_category=None, riddle_text=None, answer=None, difficulty=None):
        try:
            riddle = cls.objects.get(riddle_id=riddle_id)
            if main_category:
                riddle.main_category = main_category
            if riddle_text:
                riddle.riddle_text = riddle_text
            if answer:
                riddle.answer = answer
            if difficulty:
                riddle.difficulty = difficulty
            riddle.save()
            return riddle
        except cls.DoesNotExist:
            return None

    @classmethod
    def delete_riddle(cls, riddle_id):
        try:
            riddle = cls.objects.get(riddle_id=riddle_id)
            riddle.delete()
            return True
        except cls.DoesNotExist:
            return False


