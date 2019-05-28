from rest_framework.decorators import api_view
from common.code import *
from common.myresponse import JsonResponse
from common.token_utils import certify_token
from common.util import MyError
from user.serializers import *
import time


def get_use_to_token(token):
    if not certify_token(token):
        raise MyError(code=code_login_5000, message="token无效!")
    try:
        return UserInfo.objects.get(token=token)
    except Exception as e:
        raise MyError(code=code_login_5000, message=repr(e))


@api_view(['GET'])
def invite_friends(request):
    use = get_use_to_token(request.META['HTTP_TOKEN'])
    try:
        invite_code = request.query_params['invite_code']
    except Exception as e:
        raise MyError(code=code_params_3000, message=repr(e))

    try:
        inviter = UserInfo.objects.get(invite_code=invite_code)
    except Exception as e:
        raise MyError(code=code_login_5001, message="邀请码无效,不存在的邀请码")

    if use.invited:
        return JsonResponse(code=code_200_ok, data={}, msg="您已经被邀请,不能重复邀请")

    if use == inviter:
        return JsonResponse(code=code_200_ok, data={}, msg="您不能邀请您自己!")

    use.invited = inviter.invite_code
    use.save()
    inviter.friends.add(use)
    inviter.save()
    return JsonResponse(code=code_200_ok, data=[], msg="邀请成功!赶快去做任务吧!")


@api_view(['GET'])
def query_tickets(request):
    use = get_use_to_token(request.META['HTTP_TOKEN'])
    ticket_set = use.ticket_set.all()
    serializer = TicketSerializers(ticket_set, many=True)
    return JsonResponse(code=code_200_ok, data=serializer.data, msg='success')


def get_first_day_invite_reward(use):
    if use.progress == 1:
        use.bean += 1000
        use.progress = 2
        use.save()
        RechargeInfo.objects.create(user_info=use, bean=1000, recharge_desc='完成邀请任务第一天获得奖励')
        return JsonResponse(code=code_200_ok, data={}, msg='success')
    else:
        return JsonResponse(code=code_invite_6000, data={'current_progress': use.progress}, msg='fail')


def get_next_day_invite_reward(use):
    if use.progress == 2:
        use.bean += 3000
        use.progress = 3
        use.save()
        RechargeInfo.objects.create(user_info=use, bean=3000, recharge_desc='完成邀请任务第二天获得奖励')
        return JsonResponse(code=code_200_ok, data={}, msg='success')
    else:
        return JsonResponse(code=code_invite_6000, data={'current_progress': use.progress}, msg='fail')


def get_third_day_invite_reward(use):
    if use.progress == 3:
        use.bean += 4000
        use.progress = 4
        use.save()
        RechargeInfo.objects.create(user_info=use, bean=4000, recharge_desc='完成邀请任务第三天获得奖励')
        effective_time = int(time.time()) + 7 * 24 * 3600
        inviter = UserInfo.objects.get(invite_code=use.invited)
        Ticket.objects.create(effective_time=effective_time, user_info=inviter)
        return JsonResponse(code=code_200_ok, data={}, msg='success')
    else:
        return JsonResponse(code=code_invite_6000, data={'current_progress': use.progress}, msg='任务已完成,不能重复完成')


@api_view(['GET'])
def complete_invite_task(request):
    use = get_use_to_token(request.META['HTTP_TOKEN'])
    if not use.invited:
        return JsonResponse(code=code_200_ok, msg="您还没被邀请,不能完成此任务!")

    try:
        progress = request.query_params['progress']
    except Exception as e:
        raise MyError(code=code_params_3000, message=repr(e))
    if str(progress).__eq__('1'):
        return get_first_day_invite_reward(use)
    elif str(progress).__eq__('2'):
        return get_next_day_invite_reward(use)
    elif str(progress).__eq__('3'):
        return get_third_day_invite_reward(use)
    else:
        raise MyError(code=code_error_9999, message='不存在的任务!')


@api_view(['GET'])
def friends_list(request):
    use = get_use_to_token(request.META['HTTP_TOKEN'])
    friends = use.friends.all()
    serialize = UserSerializers(friends, many=True)
    return JsonResponse(code=code_200_ok, data=serialize.data, msg='success')
