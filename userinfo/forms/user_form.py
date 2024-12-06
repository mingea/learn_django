import hashlib
import re
from django import forms
from django.conf import settings
from app01.models import Employee
from userinfo.models import User

class edit_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','role','employee']
        # 用于表单渲染方式
        widgets = {
            "employee":forms.Select(attrs={"lay-search":""}),
        }
    # 验证用户名不能重复
    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError("用户名已存在")
        return username
    
    # md5
    def MD5(str):
        obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
        obj.update(str.encode('utf-8'))
        return obj.hexdigest()
    # 控制员工选择框只能选择没有创建用户的人员
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        user_obj = User.objects.all()
        user_id_list = [obj.employee_id for obj in user_obj]
        self.fields['employee'].queryset = Employee.objects.exclude(id__in=user_id_list)
        for name,field in self.fields.items():
            field.widget.attrs.update({"class":"layui-input","placeholder":"输入"+field.label})

# 登录表单类
class login_form(forms.ModelForm):
    # 验证码输入框
    captcha = forms.CharField(
        label='验证码',
        required=True,
        widget=forms.TextInput(attrs={'class':'layui-input'})
    )
    class Meta:
        model =User
        fields = ['username','password',"captcha"]
        widgets ={
            'password':forms.PasswordInput(attrs={"lay-affix":"eye"},render_value=True),
        }


    def clean_password(self):
        password = self.cleaned_data.get("password")
        return edit_form.MD5(password)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({"class":"layui-input","placeholder":"输入"+field.label})

# 密码修改表单类
class password_form(forms.ModelForm):
    confirm_password = forms.CharField(
        label="确认新密码",
        required=True,
        widget=forms.PasswordInput(render_value=True,attrs={"lay-affix":"eye"})
    )
    new_password = forms.CharField(
        label="新密码",
        required=True,
        widget=forms.PasswordInput(render_value=True,attrs={"lay-affix":"eye"})
    )
    class Meta:
        model =User
        fields = ['username','password','new_password','confirm_password']
        widgets ={
            'password':forms.PasswordInput(attrs={"lay-affix":"eye"},render_value=True),
        }
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({"class":"layui-input","placeholder":"输入"+field.label})


class user_add_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','employee','role']
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 循环找到所有插件添加样式
        for name,field in self.fields.items():
            # print(name,"==字段名称",field)
            field.widget.attrs={"class":"layui-input","placeholder":"输入"+field.label}