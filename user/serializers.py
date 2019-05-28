from rest_framework import serializers
from .models import *


class CompleteUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('bean', 'user_name', 'invite_code', 'email', 'pic_url',)


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('bean', 'user_name', 'invite_code',)


# class TagsSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Tags
#         fields = ('tag',)


class GoogleLoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('user_name', 'email', 'pic_url', 'bean', 'token', 'google_id', 'login_type', 'invite_code')


class FbLoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('user_name', 'email', 'pic_url', 'bean', 'token', 'fb_id', 'login_type', 'invite_code')


class LineLoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('user_name', 'email', 'pic_url', 'bean', 'token', 'login_type', 'invite_code', 'line_id')


class FriendSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('token', 'user_name', 'bean')


class RechargeSerializers(serializers.ModelSerializer):
    user_info = serializers.StringRelatedField(many=False)

    class Meta:
        model = RechargeInfo
        fields = ('recharge_time', 'bean', 'user_info', 'recharge_desc')


class ConsumeSerializers(serializers.ModelSerializer):
    user_info = serializers.StringRelatedField(many=False)

    class Meta:
        model = ConsumeInfo
        fields = ('consume_time', 'bean', 'book_name', 'chapter_name', 'chapter_count', 'user_info')


class QueryConsumeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ConsumeInfo
        fields = ('consume_time', 'bean', 'book_name', 'chapter_name', 'chapter_count')


class SignInfoSerializers(serializers.ModelSerializer):
    user_info = UserSerializers(many=False)

    class Meta:
        model = SignInfo
        fields = ('user_info', 'continuous_sign_day', 'sign_bean', 'pre_sign_day')


class TaskSerializers(serializers.ModelSerializer):
    user_info = UserSerializers(many=False)

    class Meta:
        model = TaskInfo
        fields = ('task_type', 'task_desc', 'user_info',)


class TicketSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('obtain_time', 'effective_time', 'free_ads_day', 'status',)
