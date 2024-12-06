from django.shortcuts import redirect, render,HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from userinfo.forms import user_form
from userinfo.models import User
from templates.common import res_json_data
from django.conf import settings
from userinfo.forms.user_form import edit_form,user_add_form
from django.contrib import messages
import random
from captcha.image import ImageCaptcha
from io import BytesIO
from PIL import Image

# Create your views here.
# 用户列表
@csrf_exempt
def user_list(request):
    if request.method == "GET":
        return render(request,"userinfo/user_list.html")
    page = request.POST.get('page', 1)
    limit = request.POST.get('limit', 10)
    searchParams = request.POST.get('searchParams', None)
    data_obj = User.objects.all()
    data_page = Paginator(data_obj, limit).page(page)
    data_list=[]
    count = (int(page) - 1) * int(limit)
    for row in data_page:
        count += 1
        item_dict = {}
        field_names = [field.name for field in row._meta.fields]
        for field in field_names:
            if field == "employee":
                item_dict[field] = row.employee.name
            elif field == "role":
                item_dict[field] = row.role.name
            else:
                item_dict[field] = getattr(row,field)
        item_dict["index"]=count
        data_list.append(item_dict)
    return res_json_data.table_api(data=data_list,count=len(data_obj))

# 用户添加
def user_add(request):
    if request.method == "GET":
        form = user_form.user_add_form()
        return render(request,"userinfo/user_edit.html",{"form":form})
    form = user_form.user_add_form(data=request.POST)
    if form.is_valid():
        form.instance.password = user_add_form.MD5(settings.DEFAULT_PASSWORD)
        form.save()
        messages.success(request, '添加成功')
        return render(request,"userinfo/user_edit.html",{"form":form})
    print(form.errors)
    return render(request,"userinfo/user_edit.html",{"form":form})


# 重置密码
@csrf_exempt
def reset_password(request):
    id = request.POST.get("id") #用户id
    password = edit_form.MD5(settings.DEFAULT_PASSWORD)
    User.objects.filter(id=id).update(password=password)
    return res_json_data.success_api()

# 用户登录
def user_login(request):
    if request.method == "GET":
        form = user_form.login_form()
        return render(request,"userinfo/login.html",{"form":form})
    form = user_form.login_form(data=request.POST)#获取表单数据
    if form.is_valid():#-如果表单数据有效
        print(form.cleaned_data,"===校验完成") #打印form提交的所有数据
        # 获取输入的验证码,并从form中移除
        input_captcha = form.cleaned_data.pop('captcha')
        captcha_code = request.session.get('captcha','')# 获取系统生成的验证码
        if input_captcha.upper() != captcha_code.upper():
            form.add_error("captcha","验证码错误")
            return render(request,"userinfo/login.html",{"form":form})
        user_obj = User.objects.filter(**form.cleaned_data).first()#解包清洗后的数据进行查询第一个数据
        if not user_obj:
            messages.warning(request, '用户名或密码错误')
            return render(request,"userinfo/login.html",{"form":form})
        # 登录成功，下面是保存会话信息，简单来说就是保存用户信息到服务器，方便调用request.session["user_info"] 获取这些信息。
        request.session["user_info"] = {
            "id":user_obj.id,
            "username":user_obj.username,
            "name":user_obj.employee.name,
        }
        
        request.session.set_expiry(0)
        return redirect("/employee/list/")
    

    print(form.errors)
    return render(request,"userinfo/login.html",{"form":form})

# 用户退出
def user_logout(request):
    request.session.clear()
    return redirect("/")


# 修改密码
def change_password(request):
    if request.method == "GET":
        form = user_form.password_form()
        return render(request,"common/single_edit_dlg.html",{"form":form})
    user_info = request.session['user_info']
    user_id = user_info['id']
    row_obj = User.objects.filter(id=user_id).first()
    form = user_form.password_form(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = edit_form.MD5(form.cleaned_data['password'])
        if row_obj.username != username or row_obj.password!=password:
            messages.error(request, '用户名或密码不正确')
            return render(request,"common/single_edit_dlg.html",{"form":form})
        if form.cleaned_data['new_password']!= form.cleaned_data['confirm_password']:
            messages.error(request, '两次密码输入不一致')
            return render(request,"common/single_edit_dlg.html",{"form":form})
        new_password = edit_form.MD5(form.cleaned_data['new_password'])
        User.objects.filter(id=user_id).update(password=new_password)
        messages.success(request, '修改成功')
        return render(request,"common/single_edit_dlg.html",{"form":form})
    
    return render(request,"common/single_edit_dlg.html",{"form":form})



# 生成验证码
def get_catpcha(request):
    code = random.sample('abcdefghijklmnopqrstuvwxyz', 4)
    request.session['captcha'] = ''.join(code) #转为字符串，存储到session中
    # 转换code为大写字母
    code = ''.join(code).upper()
    # 生成图片验证码对象
    captcha = ImageCaptcha()
    data = captcha.generate(code) #生成图像二进制数据
    image =Image.open(data)
    out = BytesIO()
    image.save(out,'png')  #保存图像数据，实现格式转换，写入内存
    out.seek(0)
    
    return HttpResponse(out.read(), content_type='image/png')
