class SVIPPermission(object):
    message = '必须是SVIP才能访问'
    def has_permission(self, request, view):
        if request.user.user_type !=3:
            return False
        return True

class MyPermission1(object):

    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True


        