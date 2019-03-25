from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
# from rest_framework.request import Request
from rest_framework import exceptions
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

class AuthView(APIView):
    """For user login"""

    authentication_classes = []

    def post(self, request, *args, **kwargs):
        print(list(request._request.POST))
        print(request.method)
        print(request.body)
        ret = { 'code': 1000, 'msg': None }
        try: 
            user = request._request.POST.get('username')
            # user = request._request.POST['username'

            print(user)

            pwd = request._request.POST.get('password')
            print(pwd)
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            print(obj)
            if not obj:
                ret['code'] = 1001
                ret['msg'] = "用户名或密码错误"

            token = md5(user)  
            models.UserToken.objects.update_or_create(user=obj, defaults={'token':token})          
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
            
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
    """for customer orders"""

    # authentication_classes = [Authentication, ]

    def get(self, request, *args, **kwargs):
        # token = request._request.GET.get('token')
        # if not token:
        #     return HttpResponse('用户未登录')

        # self.dispatch

        # request.user
        # request.auth
        ret = {
            'code':1000, 
            'msg': None
        }
        try: 
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)

class UserInfoView(APIView):

    # authentication_classes = [Authentication,]

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return HttpResponse('用户信息')