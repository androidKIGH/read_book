from django.http import HttpResponse
from rest_framework.views import APIView
from user.serializers import *
from common.token_utils import *
import json
from common.config import *
from urllib.request import Request, urlopen
from common.code import *
from common.util import *

logger = logging.getLogger('login')


class SystemDetection(APIView):
    def get(self, request):
        logger.info('success')
        return HttpResponse(str(int(time.time())))


class GoogleLogin(APIView):
    def post(self, request):
        post_data = request.data
        try:
            access_token = post_data['access_token']
        except Exception as e:
            raise MyError(code=code_params_3000, message=repr(e))

        google_userinfo = self.verify_and_get(access_token)

        if not google_userinfo:
            return JsonResponse(code=code_login_5001, msg="用户信息校验失败,无效的认证!")

        if not self.check_info_is_exit(google_userinfo):
            data = self.create_google_data(google_userinfo)
            data['invite_code'] = create_invite_code(UserInfo.objects.values('invite_code'))
            serializer = GoogleLoginSerializers(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(code=code_200_ok, data=serializer.data, msg="success")
        else:
            u = UserInfo.objects.get(google_id=google_userinfo['sub'])
            u.token = create_token()
            u.save()
            serializer = GoogleLoginSerializers(u)
            return JsonResponse(code=code_200_ok, data=serializer.data, msg="success")

    @staticmethod
    def verify_and_get(access_token):
        url = google_login_url.format(access_token)
        for retry in range(3):
            try:
                req = Request(url, headers={'User-Agent': USER_AGENT})
                url_socket = urlopen(req, timeout=60)
                response_body = url_socket.read()
                status = url_socket.code
                url_socket.close()
                if status == 200 and response_body:
                    resp_data = json.loads(response_body)
                    logging.info(resp_data)
                    return resp_data
            except Exception as e:
                logger.error(str(e))
        return None

    @staticmethod
    def check_info_is_exit(info):
        id_dict = UserInfo.objects.all().values('google_id')
        for ll in id_dict:
            if info['sub'] == ll['google_id']:
                return True
        return False

    @staticmethod
    def create_google_data(info):
        data = {'login_type': 'google', 'token': create_token(24 * 3600 * 30 * 12), 'bean': 0, 'google_id': info['sub']}
        if 'picture' in info.keys():
            data['pic_url'] = info['picture']

        if 'name' in info.keys():
            data['user_name'] = info['name']

        if 'email' in info.keys():
            data['email'] = info['email']

        return data


class FbLogin(APIView):
    def post(self, request):
        post_data = request.data
        try:
            user_id = post_data['user_id']
            access_token = post_data['access_token']
        except Exception as e:
            raise MyError(code_params_3000, message=repr(e))

        # self.check_info_is_exit({'id': '58695545'})
        userinfo = self.verify_and_get(user_id, access_token)

        if not userinfo:
            return JsonResponse(code=code_login_5001, msg="用户信息校验失败,无效的认证!")
        if not self.check_info_is_exit(userinfo):
            data = self.create_data(userinfo)
            data['invite_code'] = create_invite_code(UserInfo.objects.values('invite_code'))
            serializer = FbLoginSerializers(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(code=code_200_ok, data=serializer.data, msg="success")
        else:
            u = UserInfo.objects.filter(fb_id=userinfo['id']).first()
            u.token = create_token()
            u.save()
            serializer = FbLoginSerializers(u)
            return JsonResponse(code=code_200_ok, data=serializer.data, msg="success")

    @staticmethod
    def verify_and_get(user_id, access_token):
        url = fb_login_url.format(user_id=user_id, access_token=access_token)
        for retry in range(3):
            try:
                req = Request(url, headers={'User-Agent': USER_AGENT})
                url_socket = urlopen(req, timeout=60)
                response_body = url_socket.read()
                status = url_socket.code
                url_socket.close()
                if status == 200 and response_body:
                    resp_data = json.loads(response_body)
                    logging.info('fb_token_info={}'.format(resp_data))
                    return resp_data

            except Exception as e:
                logger.error(str(e))
        return None

    @staticmethod
    def create_data(info):
        data = {'login_type': 'fb', 'token': create_token(24 * 3600 * 30 * 12), 'bean': 0, 'fb_id': info['id']}
        if 'picture' in info.keys():
            data['pic_url'] = 'http://graph.facebook.com/{fb_id}/picture?type=large'.format(fb_id=info['id'])

        if 'name' in info.keys():
            data['user_name'] = info['name']

        if 'email' in info.keys():
            data['email'] = info['email']

        return data

    @staticmethod
    def check_info_is_exit(info):
        id_dict = UserInfo.objects.all().values('fb_id')
        for ll in id_dict:
            if info['id'] == ll['fb_id']:
                return True
        return False


class LineLogin(APIView):
    def post(self, request):
        post_data = request.data
        try:
            access_token = post_data['access_token']
            name = post_data['name']
            pic_url = post_data['pic_url']
            userId = post_data['userId']
        except Exception as e:
            raise MyError(code=code_params_3000, message=repr(e))

        userinfo = self.verify_and_get(access_token)
        if not userinfo:
            return JsonResponse(code=code_login_5001, msg="用户信息校验失败,无效的认证!")
        if not self.check_info_is_exit(userId):
            data = self.create_data(userId)
            data['user_name'] = name
            data['pic_url'] = pic_url
            data['invite_code'] = create_invite_code(UserInfo.objects.values('invite_code'))
            data['line_id'] = userId
            serializer = LineLoginSerializers(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(code=code_200_ok, data=serializer.data, msg="success")
        else:
            u = UserInfo.objects.filter(line_id=userId).first()
            u.token = create_token()
            u.save()
            serializer = LineLoginSerializers(u)
            return JsonResponse(code=code_200_ok, data=serializer.data, msg="success")

    @staticmethod
    def verify_and_get(access_token):
        url = line_line_url.format(access_token)
        for retry in range(3):
            try:
                req = Request(url, headers={'User-Agent': USER_AGENT})
                url_socket = urlopen(req, timeout=60)
                response_body = url_socket.read()
                status = url_socket.code
                url_socket.close()
                if status == 200 and response_body:
                    resp_data = json.loads(response_body)
                    logging.info('line_info={}'.format(resp_data))
                    return resp_data
            except Exception as e:
                logger.error(str(e))
        return None

    @staticmethod
    def check_info_is_exit(info):
        id_dict = UserInfo.objects.all().values('line_id')
        for ll in id_dict:
            if info == ll['line_id']:
                return True
        return False

    @staticmethod
    def create_data(info):
        data = {'login_type': 'line', 'token': create_token(24 * 3600 * 30 * 12), 'bean': 0,
                'line_id': info}
        return data


def get_use_to_token(token):
    if not certify_token(token):
        raise MyError(code=code_login_5000, message="token 过期")
    try:
        return UserInfo.objects.get(token=token)
    except Exception as e:
        raise MyError(code=code_login_5000, message=repr(e))


class GetUserInfo(APIView):
    def get(self, request):
        use = get_use_to_token(request.META['HTTP_TOKEN'])
        serializer = CompleteUserSerializers(use, many=False)
        return JsonResponse(code=code_200_ok, data=serializer.data, msg="success")
