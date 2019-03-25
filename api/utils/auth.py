from rest_framework import exceptions
from api import models


class FirstAuthentication(object):
    def authenticate(self, request):
        pass

    def authenticate_header(self, request):
        pass

class Authentication(object):

    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')

        return (token_obj.user, token_obj)  
        """ 
        return them to request for subsequent request by the browser
        token_obj.user  -> request.user
        token_obj  -> request.auth
        """

    def authenticate_header(self, request):  ## will cause error without this
        pass