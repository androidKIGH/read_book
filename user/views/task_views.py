from rest_framework.views import APIView
from common.code import *
from common.token_utils import certify_token
from common.util import MyError, JsonResponse
from user.serializers import *
from datetime import *
from user.constant import task_type


def get_use_to_token(token):
    if not certify_token(token):
        raise MyError(code=code_login_5000, message="token 过期")

    try:
        return UserInfo.objects.get(token=token)
    except Exception as e:
        raise MyError(code=code_login_5000, message=repr(e))


def save_to_recharge_info(use, bean, desc):
    RechargeInfo.objects.create(user_info=use, bean=bean, recharge_desc=desc)
    use.bean += bean
    use.save()


class Sign(APIView):
    def get(self, request):
        use = get_use_to_token(request.META['HTTP_TOKEN'])
        user_sign_info = SignInfo.objects.filter(user_info=use).order_by('pre_sign_day').last()
        today = date.today()
        yesterday = today - timedelta(days=1)

        if not user_sign_info:
            user_sign_info = SignInfo.objects.create(user_info=use, pre_sign_day=str(today))
            save_to_recharge_info(use, 50, '首日签到奖励！')
        else:
            pre_sign_day = user_sign_info.pre_sign_day
            if pre_sign_day.__eq__(str(today)):
                return JsonResponse(code=code_task_4000, data=SignInfoSerializers(user_sign_info, many=False).data,
                                    msg="今日已签到！")
            if pre_sign_day.__eq__(str(yesterday)):
                # 续签
                continuous_sign_day = user_sign_info.continuous_sign_day
                continuous_sign_day += 1
                if continuous_sign_day > 7:
                    continuous_sign_day = 1

                if continuous_sign_day == 3 or continuous_sign_day == 4:
                    daily_bean = 100
                elif continuous_sign_day == 6 or continuous_sign_day == 5:
                    daily_bean = 200
                elif continuous_sign_day == 7:
                    daily_bean = 500
                else:
                    daily_bean = 50
                user_sign_info = SignInfo.objects.create(user_info=use, pre_sign_day=str(today),
                                                         sign_bean=daily_bean, continuous_sign_day=continuous_sign_day)
                save_to_recharge_info(use, daily_bean, '连续签到{}天奖励！'.format(continuous_sign_day))

            else:
                # 断签
                user_sign_info = SignInfo.objects.create(user_info=use, pre_sign_day=str(today))
                save_to_recharge_info(use, 50, '首日签到奖励！')

        serializer = SignInfoSerializers(user_sign_info, many=False)
        return JsonResponse(data=serializer.data, code=code_200_ok, msg="success")


def done_user_task(_task_type, task_desc, use):
    if int(_task_type) == task_type.READ_G_TYPE:
        bean = 60
        task_desc = '阅读获取金币！'
    elif int(_task_type) == task_type.READ_REWARD_G_TYPE:
        bean = 60
        task_desc = '观看激励视频获取金币！'
    elif int(_task_type) == task_type.SIGN_REWARD_G_TYPE:
        continuous_sign_day = SignInfo.objects.filter(user_info=use).order_by('pre_sign_day').last().continuous_sign_day
        if continuous_sign_day >= 8:
            continuous_sign_day = 1
        if continuous_sign_day == 3 or continuous_sign_day == 4:
            daily_bean = 100
        elif continuous_sign_day == 6 or continuous_sign_day == 5:
            daily_bean = 200
        elif continuous_sign_day == 7:
            daily_bean = 500
        else:
            daily_bean = 50
        bean = daily_bean
        task_desc = '签到获取金币观看激励视频！'
    elif int(_task_type) == task_type.SHARE_G_TYPE:
        bean = 50
        task_desc = '分享获取金币！'
    elif int(_task_type) == task_type.SHARE_REWARD_G_TYPE:
        bean = 50
        task_desc = '分享获取金币观看激励视频！'
    elif int(_task_type) == task_type.WHELL_G_TYPE:
        bean = 100
        task_desc = '转盘获取金币！'
    elif int(_task_type) == task_type.WHELL_REWARD_G_TYPE:
        bean = 100
        task_desc = '转盘获取金币观看激励视频！'
    elif int(_task_type) == task_type.TASK_NEW_LOOK_RULE:
        bean = 200
        task_desc = '新手任务 - 查看用户手册！'
    elif int(_task_type) == task_type.TASK_NEW_LOOK_REWARD_RULE:
        bean = 200
        task_desc = '新手任务 - 查看用户手册激励视频！'
    elif int(_task_type) == task_type.TASK_NEW_LOOK_CION:
        bean = 100
        task_desc = '新手任务 - 查看我的金币！'
    elif int(_task_type) == task_type.TASK_NEW_LOOK_REWARD_CION:
        bean = 100
        task_desc = '新手任务 - 查看我的金币激励视频！'
    elif int(_task_type) == task_type.TASK_NEW_NEW_WELFACE:
        bean = 2000
        task_desc = '新人登录专属好礼！'
    elif int(_task_type) == task_type.TASK_REWARD_COIN:
        bean = 30
        task_desc = '观看激励视频获取金币！'
    elif int(_task_type) == task_type.TASK_UPDATE_COIN:
        bean = 100
        task_desc = 'APP升级获取金币！'
    elif int(_task_type) == task_type.TASK_FILL_QUESTIONS:
        bean = 300
        task_desc = '填写问卷获得奖励！'
    elif int(_task_type) == task_type.TASK_FILL_QUESTIONS_REWARD_COIN:
        bean = 300
        task_desc = '填写问卷观看激励视频获得奖励！'
    else:
        raise MyError(code=code_task_4002, message="任务不存在！")

    save_to_recharge_info(use=use, bean=bean, desc=task_desc)
    serializer = TaskSerializers(TaskInfo.objects.create(user_info=use, task_type=str(_task_type), task_desc=task_desc))
    return JsonResponse(code=code_200_ok, data=serializer.data, msg='success!')


class Task(APIView):
    def get(self, request):
        use = get_use_to_token(request.META['HTTP_TOKEN'])
        try:
            _task_type = request.query_params['task_type']
        except Exception as e:
            raise MyError(code=code_params_3000, message=repr(e))

        if int(_task_type) in task_type.new_user_task:
            # 新手任务
            return self.new_user_task_done(_task_type, use)

        elif int(_task_type) in task_type.daily_task:
            # 日常任务
            return self.daily_task_done(_task_type, use)

        elif int(_task_type) in task_type.normal_task:
            # 普通任务
            return done_user_task(_task_type, None, use)
        else:
            raise MyError(code=code_task_4002, message="任务不存在！")

    @staticmethod
    def daily_task_done(_task_type, use):
        last_task = use.taskinfo_set.filter(task_type=_task_type).order_by('task_time').last()
        if not last_task:
            return done_user_task(_task_type, None, use)

        last_time = last_task.task_time
        if last_time.__eq__(date.today()):
            return JsonResponse(code=code_task_4003, data={}, msg='今日任务已完成！')
        else:
            return done_user_task(_task_type, None, use)

    @staticmethod
    def new_user_task_done(_task_type, use):
        use_set = TaskInfo.objects.filter(user_info=use)
        if not use_set:
            return done_user_task(_task_type, None, use)
        else:
            type_list = use_set.values_list('task_type')
            for task in type_list:
                if str(_task_type) in task:
                    return JsonResponse(code=code_task_4001, data={}, msg='任务已完成！')
            else:
                return done_user_task(_task_type, None, use)


class GetRechargeInfo(APIView):
    size = 30

    def get(self, request):
        try:
            index = request.query_params['index']
        except Exception as e:
            raise MyError(code=code_params_3000, message=repr(e))

        use = get_use_to_token(request.META['HTTP_TOKEN'])

        recharge_set = RechargeInfo.objects.filter(user_info=use).order_by('-recharge_time')[
                       int(index) * GetRechargeInfo.size:(int(index) + 1) * GetRechargeInfo.size]

        serializer = RechargeSerializers(recharge_set, many=True)
        return JsonResponse(code=code_200_ok, data=serializer.data, msg="success")


class ExchangeAds(APIView):
    day_ads = "0"
    week_ads = "1"
    mouth_ads = "2"

    def get(self, request):
        try:
            exchange_type = request.query_params['exchange_type']
        except Exception as e:
            raise MyError(code=code_params_3000, message=repr(e))

        use = get_use_to_token(request.META['HTTP_TOKEN'])
        if str(exchange_type).__eq__(ExchangeAds.week_ads):
            pay_bean = 64999
            desc = '兑换一周广告'

        elif str(exchange_type).__eq__(ExchangeAds.mouth_ads):
            pay_bean = 170000
            desc = '兑换一个月广告'
        elif str(exchange_type).__eq__(ExchangeAds.day_ads):
            pay_bean = 9999
            desc = '兑换一天广告'
        else:
            raise MyError(code=code_params_3000, message="不存在的任务")

        if use.bean < pay_bean:
            return JsonResponse(code=code_error_9999, data={}, msg="金币余额不足！")

        save_to_recharge_info(use=use, bean=-pay_bean, desc=desc)
        serializer = UserSerializers(use, many=False)

        return JsonResponse(code=code_200_ok, data=serializer.data, msg="success")


class GetTaskInfo(APIView):
    def get(self, request):
        use = get_use_to_token(request.META['HTTP_TOKEN'])
        Jsondata = {}

        # 签到信息
        user_sign_info = SignInfo.objects.filter(user_info=use).order_by('pre_sign_day').last()

        Jsondata['sign_info'] = SignInfoSerializers(user_sign_info, many=False).data

        task_new_user = {'look_rule': False, 'look_coin': False, 'fill_question': False}

        use_set = TaskInfo.objects.filter(user_info=use)
        type_list = use_set.values_list('task_type')

        for task in type_list:
            if str(task_type.TASK_NEW_LOOK_RULE) in task:
                task_new_user['look_rule'] = True
            elif str(task_type.TASK_NEW_LOOK_CION) in task:
                task_new_user['look_coin'] = True
            elif str(task_type.TASK_FILL_QUESTIONS) in task:
                task_new_user['fill_question'] = True

        Jsondata['task_new_user'] = task_new_user

        return JsonResponse(code=code_200_ok, data=Jsondata, msg='success!')
