from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from datetime import datetime
class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("===访问地址:",request.path,datetime.now())
        pass_urls = ['/',"/image/code/"]
        if request.path  in pass_urls:
            return
        
        user_info = request.session.get('user_info')
        print(user_info,"==登陆用户信息")
        # 检查用户是否登陆，是就继续，否就跳转登录页面
        if  user_info:
            return
        return redirect("/")
    

