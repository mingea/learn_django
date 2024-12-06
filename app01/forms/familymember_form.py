from django import forms
from app01.models import FamilyMember

class familymember_add_form(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['employee','name','relationship']
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 循环找到所有插件添加样式
        for name,field in self.fields.items():
            # print(name,"==字段名称",field)
            field.widget.attrs={"class":"layui-input","placeholder":"输入"+field.label}
        