from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from api import models

def md5(user):        #### generating random string
    import hashlib
    import time

    ctime = str(time.time())  ## converting current time into a string
    
    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()

class AuthView(APIView):

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