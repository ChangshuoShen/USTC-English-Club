from django.db import models, connection
from django.contrib.auth.hashers import make_password
from django.utils import timezone


# 用户信息
class User(models.Model):
    # 一些用户的相关属性
    name = models.CharField(verbose_name='name', max_length=64, blank=False, )
    gender = models.CharField(verbose_name='gender', max_length=10, null=True, blank=True)

    email = models.EmailField(verbose_name='email', unique=True)
    password = models.CharField(verbose_name='password', max_length=256, blank=False)

    birthdate = models.DateField(verbose_name='birthdate', null=True, blank=True)
    register_date = models.DateTimeField(verbose_name='register_date', default=timezone.now)

    @classmethod
    def create_user(cls, name='guest', gender='male', email=None, raw_password=None, birthdate=None):
        """
        创建用户并设置密码
        """
        user = cls(
            name=name,
            gender=gender,
            email=email,
            birthdate=birthdate,
            register_date=timezone.now()
        )

        # 使用 make_password 函数对密码进行哈希处理
        user.set_password(raw_password)
        # 注意之后进行验证的时候使用check_password方法，而不是使用
        user.save()
        return user

    @classmethod
    def get_user_by_email(cls, email):
        try:
            user = cls.objects.get(email=email)
            return user
        except cls.DoesNotExist:
            return None


    @classmethod
    def custom_query(cls, *fields, **kwargs):
        '''
        传入位置参数查询相关字段，如果没有传入那就直接查询 * 了
        '''
        query = "SELECT {fields} FROM {table_name}".format(
            fields=", ".join(fields) if fields else "*",
            table_name=cls._meta.db_table
            # meta类用于提供元数据metadata，包括数据库的名称，数据库的排序顺序，特定的数据库表选项
        )
        conditions = []     # kwargs传入字段名称-字段值的键值对
        params = []

        for field, value in kwargs.items():
            if value is not None:
                conditions.append("{field} = %s".format(field=field))
                params.append(value)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        # 一般使用时查询结果至多一个
        if not rows:
            return None
        else:
            result_dict = {}
            for i, field_value in enumerate(rows[0]):
                field_name = fields[i] if fields else cls._meta.fields[i].name
                result_dict[field_name] = field_value
            print(result_dict)
            return result_dict

    def check_password(self, raw_password):
        """
        检查密码是否匹配
        """
        return raw_password == self.password

    def get_age(self):
        """
        获取用户年龄
        """
        if self.birthdate:
            today = timezone.now()
            age = today.year - self.birthdate.year - (
                        (today.month, today.day) < (self.birthdate.month, self.birthdate.day))
            return age
        else:
            return None

    def set_password(self, raw_password):
        """
        设置用户密码并进行哈希处理
        """
        self.password = make_password(raw_password)
        self.save()

    def get_full_name(self):
        """
        获取用户完整姓名
        """
        return self.name

    # class Meta:
    #     db_table = "accounts_user"

'''
# 邮箱验证
class EmailVerifyRecord(models.Model):

    # 验证码
    code = models.CharField(max_length=20, verbose_name="verification_code")
    email = models.EmailField(max_length=50, verbose_name="email")

    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name="send_type", max_length=10,
                                 choices=(("register", "注册"), ("forget", "找回密码")))
    send_time = models.DateTimeField(verbose_name="发送时间", default=timezone.now)

    class Meta:
        verbose_name = u"2. 邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)
'''
