from django.urls import path

from user.views import task_views
from user.views import login_views, invite_views

urlpatterns = [
    # 服务器监测
    path('system_detection', login_views.SystemDetection.as_view()),
    # 用户信息
    path('login_google', login_views.GoogleLogin.as_view()),
    path('login_fb', login_views.FbLogin.as_view()),
    path('login_line', login_views.LineLogin.as_view()),
    path('get_userinfo', login_views.GetUserInfo.as_view()),

    # 任务api
    path('get_task_info', task_views.GetTaskInfo.as_view()),

    path('daily_sign', task_views.Sign.as_view()),
    path('task', task_views.Task.as_view()),

    path('get_rechargeInfo', task_views.GetRechargeInfo.as_view()),
    path('exchange_ads', task_views.ExchangeAds.as_view()),
    path('invite_friends', invite_views.invite_friends),
    path('friends_list', invite_views.friends_list),
    path('complete_invite_task', invite_views.complete_invite_task),
    path('query_tickets', invite_views.query_tickets),

]
