import time
import base64
import hmac
import random

key = 'webeye-qingyan-noval-s'


# 生成token
def create_token(expire=3600 * 12 * 24):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


# 检验TOKEN
def certify_token(token):
    try:
        token_str = base64.urlsafe_b64decode(token).decode('utf-8')
        token_list = token_str.split(':')
        if len(token_list) != 2:
            return False
        ts_str = token_list[0]
        if float(ts_str) < time.time():
            # token expired
            return False
        known_sha1_tsstr = token_list[1]
        sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
        calc_sha1_tsstr = sha1.hexdigest()
        if calc_sha1_tsstr != known_sha1_tsstr:
            # token certification failed
            return False
            # token certification success
    except:
        return False
    return True


def __create_code():
    tt = 'qwertyuiopalskdjfhgm884750209236511znxbcvQWERTYUIOPALSKDJFHGMZNXBCV1234567890'
    invite_code = ''
    while len(invite_code) < 6:
        r = random.randint(0, 62)
        invite_code += tt[r]
    return invite_code


def create_invite_code(invite_list):
    while True:
        invite_code = __create_code()
        if invite_code not in invite_list:
            return invite_code
