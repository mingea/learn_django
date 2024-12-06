import re
from django import forms
from app01.models import Employee
class employee_add_form(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name','depart','job_number','gender','birthday']
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 循环找到所有插件添加样式
        for name,field in self.fields.items():
            # print(name,"==字段名称",field)
            field.widget.attrs={"class":"layui-input","placeholder":"输入"+field.label}
        
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not re.match(r'^1[3-9]\d{9}$', phone):
                raise forms.ValidationError('请输入有效的手机号码。')    

        return phone
class employee_seacher_form(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name','gender','depart','job_number','phone']
        widgets = {
            "gender":forms.Select(attrs={"lay-filter":"select-filter"}),
            "depart":forms.Select(attrs={"lay-filter":"select-filter"}),
        }
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({"class":"layui-input","placeholder":"输入"+field.label})



