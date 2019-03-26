from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
# from rest_framework.request import Request
from rest_framework import exceptions
from api.utils.permission import SVIPPermission, MyPermission1
from api import models

ORDER_DICT = {
    1:{
        'name':"piano",
        'age': 18,
        'gender': '女',
        'content': '...'
    },
    2:{
        'name':"violin",
        'age': 33,
        'gender': '男',
        'content': 'hall'
    },
}

def md5(user):        #### generating random string
    import hashlib
    import time

    ctime = str(time.time())  ## converting current time into a string
    
    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()

from rest_framework.throttling import BaseThrottle
import time

VISIT_RECORD = {}

class VisitThrottle(BaseThrottle):

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        # remote_addr = request._request.META.get('REMOTE_ADDR')
        remote_addr = request.META.get('REMOTE_ADDR')
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime,]
            return True

        history = VISIT_RECORD.get(remote_addr)
        self.history = history

        while history and history[-1] < ctime - 60:  ## only 3 visits per 10 seconds allowed
            history.pop()

        if len(history) < 3:
            history.insert(0, ctime)
            return True
        # return True # return false meaning visit freqency too high, being limited 
        # return True

    def wait(self):
        ctime = time.time()
        return 60 - (ctime - self.history[-1])


class AuthView(APIView):
    """For user login"""

    authentication_classes = []
    permission_classes = []
    throttle_classes = [VisitThrottle, ]

    def post(self, request, *args, **kwargs):
        # print(list(request._request))
        # print(request.method)
        # print(request.body)
        ret = { 'code': 1000, 'msg': None }
        try: 
            user = request._request.POST.get('username')

            # print(user)

            pwd = request._request.POST.get('password')
            # print(pwd)
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            # print(obj)
            if not obj:
                ret['code'] = 1001
                ret['msg'] = "用户名或密码错误"

            token = md5(user)  
            models.UserToken.objects.update_or_create(user=obj, defaults={'token':token})          
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常访问'
            
        return JsonResponse(ret)

# class Authentication(object):

#     def authenticate(self, request):
#         token = request._request.GET.get('token')
#         token_obj = models.UserToken.objects.filter(token=token).first()
#         if not token_obj:
#             raise exceptions.AuthenticationFailed('用户认证失败')

#         return (token_obj.user, token_obj)  
#         """ 
#         return them to request for subsequent request by the browser
#         token_obj.user  -> request.user
#         token_obj  -> request.auth
#         """

#     def authenticate_header(self, request):  ## will cause error without this
#         pass

class OrderView(APIView):
    """for customer orders (for SVIP only)"""

    # authentication_classes = [Authentication, ]
    # permission_classes = [SVIPPermission,]

    def get(self, request, *args, **kwargs):

        # if request.user.user_type != 3:
        #     print(request.user.username)
        #     return HttpResponse('无权访问')
       
        # print(request.user.username)
        ret = {
            'code':1000, 
            'msg': None,
            'data': None
        }
        try: 
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)

# from rest_framework.authentication import BaseAuthentication, BasicAuthentication

class UserInfoView(APIView):

    # authentication_classes = [BasicAuthentication,]
    permission_classes = [MyPermission1,]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 3:
            return HttpResponse('无权访问')
        # print(request.user)
        # print(request.auth)
        return HttpResponse('用户信息')