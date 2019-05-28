from django.db import models
from datetime import *


class RechargeInfo(models.Model):
    bean = models.IntegerField()
    money = models.FloatField(null=True)
    recharge_time = models.DateTimeField(auto_now_add=True)
    user_info = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    recharge_desc = models.CharField(max_length=100, default='')

    class Meta:
        ordering = ('recharge_time',)


class UserInfo(models.Model):
    user_name = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField(max_length=100, blank=True, default='')
    pic_url = models.CharField(max_length=200, blank=True, default='')
    first_login_time = models.DateTimeField('首次登录时间', auto_now_add=True)
    last_login_time = models.DateTimeField("最近活动时间", auto_now=True)
    fb_id = models.CharField(max_length=100, null=True)
    google_id = models.CharField(max_length=100, null=True)
    line_id = models.CharField(max_length=100, null=True)
    bean = models.IntegerField(default=0)
    invite_code = models.CharField(max_length=10)
    login_type = models.CharField(max_length=10)
    token = models.CharField(max_length=200)
    invited = models.CharField(max_length=10, null=True)
    friends = models.ManyToManyField('self', symmetrical=False)
    progress = models.IntegerField('完成邀请任务的进度', default=1)

    class Meta:
        ordering = ('first_login_time',)

    def __str__(self):
        return self.user_name


class ConsumeInfo(models.Model):
    consume_time = models.DateTimeField(auto_now_add=True)
    bean = models.IntegerField()
    book_name = models.CharField(max_length=30)
    chapter_name = models.CharField(max_length=30)
    chapter_count = models.IntegerField()
    user_info = models.ForeignKey('UserInfo', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)


class SignInfo(models.Model):
    user_info = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    continuous_sign_day = models.IntegerField(default=1)
    pre_sign_day = models.CharField(max_length=30)
    sign_bean = models.IntegerField(default=50)

    class Meta:
        ordering = ('id',)


class TaskInfo(models.Model):
    task_type = models.CharField(max_length=20)
    task_desc = models.CharField(max_length=100, default='')
    user_info = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    task_time = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('id',)


class Ticket(models.Model):
    obtain_time = models.DateTimeField('券获得时间', auto_now_add=True)
    effective_time = models.CharField('券有效时间', max_length=20)
    free_ads_day = models.IntegerField('免广告的天数', default=1)
    status = models.BooleanField('券是否已经使用', default=False)
    user_info = models.ForeignKey('UserInfo', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
