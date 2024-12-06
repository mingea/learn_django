from django.shortcuts import render,HttpResponse,redirect
from app01.models import Department,Employee,FamilyMember
from app01.forms import employee_form,familymember_form
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from templates.common import res_json_data
import json
from django.contrib import messages

# Create your views here.
def index(request):
    return HttpResponse('Hello')

# 部门列表
def depart_list(request):
    data_list = Department.objects.all()
    for obj in data_list:
        print(obj.id,obj.name)
    return render(request,'archives/depart_list.html',{"data_list":data_list})

# 添加部门
def depart_add(request):
    # print(request.method,"==请求方式")
    # if request.method == "GET":
    #     return render(request,"archives/depart_add.html")
    # print(request.POST,"==POST请求数据")
    # return HttpResponse("添加部门操作")
    name = request.POST.get("name")
    index = request.POST.get("index")
    if name:
        Department.objects.create(name=name,index=index)
        return redirect("/depart/list/")
    return render(request,"archives/depart_add.html",{'title':'添加部门'})
# 部门数据编辑
def depart_edit(request,nid):
    if request.method == "GET":
        row_obj = Department.objects.filter(id=nid).first()
        return render(request,"archives/depart_add.html",{"row_obj":row_obj,'title':'编辑部门'})
    name = request.POST.get("name")
    index = request.POST.get("index")
    row_obj = Department.objects.filter(id=nid).first()
    row_obj.name = name
    row_obj.index = index
    row_obj.save()
    return redirect("/depart/list/")

# 部门数据删除
def depart_del(request,nid):
    Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")

# 员工添加
def employee_add(request):
    if request.method == "GET":
        form = employee_form.employee_add_form()
        # for field in form:
            # print(field,"==字段控件")
            # print(field.label,"==字段标签")
            # print(field.name,"==字段名称")
            # print(field.field.required,"==字段是否必输")
        return render(request,"archives/employee_add.html",{"form":form,'title':'添加员工'})

    # 用户提交数据检验
    form = employee_form.employee_add_form(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data) #打印form提交的所有数据
        form.instance.hiredate=datetime.now()
        form.save()
        return redirect("/employee/list/")
    # print(form.errors) #打印form提交的错误信息
    return render(request,"archives/employee_add.html",{"form":form,'title':'添加员工'})
# 员工数据表格
@csrf_exempt
def employee_list(request):
    # for i in range(100):
    #     new_data ={
    #         'name':f"员工{i}",
    #         'job_number':f"RS0{i}",
    #         'gender':1,
    #         'birthday':'2018-08-11',
    #         'hiredate':datetime.now(),
    #         'depart':Department.objects.first(),
    #     }
    #     # Employee.objects.create(**new_data)
    #     employee =Employee(**new_data)
    #     employee.save()
    print(request.method,"==请求方式")
    if request.method == "GET":
        init_data ={"gender":0}
        form =employee_form.employee_seacher_form(initial=init_data)
        return render(request,"archives/employee_list.html",{"form":form})
    
    # post请求返回JSON
    page = request.POST.get('page', 1)
    limit = request.POST.get('limit', 10)
    searchParams = request.POST.get('searchParams', None)
    if searchParams:
        searchParams =json.loads(searchParams)
        fileld_names = list(searchParams.keys())
        fileld_vaules = list(searchParams.values())
        filter_dict = dict()
        for i in range(len(fileld_vaules)):
            if fileld_vaules[i]:
                if fileld_names[i] == "depart":
                    item = fileld_names[i]+"_id"
                else:
                    item = fileld_names[i]+"__contains"
                filter_dict[item] = fileld_vaules[i]
        print(filter_dict,"==查询参数")
        data_obj = Employee.objects.filter(**filter_dict).order_by('-id')
    else:
        data_obj = Employee.objects.all().order_by('-id')
    data_page = Paginator(data_obj, limit).page(page)
    data_list=[]
    count = (int(page) - 1) * int(limit)
    for row in data_page:
        count += 1
        item_dict = {}
        field_names = [field.name for field in row._meta.fields] # Model._meta.fields :返回模型字段对象列表
        for field in field_names:
            if field == "depart":
                item_dict[field] = row.depart.name
            elif field == "gender":
                item_dict[field] = row.get_gender_display()
            else:
                item_dict[field] = getattr(row,field)

        data_list.append(item_dict)
    return res_json_data.table_api(data=data_list,count=len(data_obj))


# 员工数据编辑
def employee_edit(request,nid):
    row_obj = Employee.objects.filter(id=nid).first()
    if request.method == "GET":
        form = employee_form.employee_add_form(instance=row_obj)
        return render(request,"archives/employee_add.html",{"form":form,'title':'编辑员工'})
    
    form = employee_form.employee_add_form(data=request.POST,instance=row_obj)
    if form.is_valid():
        form.save()
        messages.success(request, '编辑成功')
        return render(request,"archives/employee_list.html",{"form":form})
    print(form.errors,"===表单校验错误")
    return render(request,"archives/employee_add.html",{"form":form,'title':'编辑员工'})
# 员工删除
def employee_del(request,nid):
    Employee.objects.filter(id=nid).delete()
    return redirect("/employee/list/")

# 家庭成员表格
def familymember_list(request):
    data_list = FamilyMember.objects.all()
    return render(request,"archives/familymember_list.html",{"data_list":data_list})


# 家人添加
def familymember_add(request):
    if request.method == "GET":
        form = familymember_form.familymember_add_form()
        return render(request,"archives/familymember_add.html",{"form":form,'title':'添加家庭成员'})

    # 用户提交数据检验
    form = familymember_form.familymember_add_form(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data) #打印form提交的所有数据
        print(form.cleaned_data['employee'])
        form.save()
        return redirect("/familymember/list/")
    # print(form.errors) #打印form提交的错误信息
    return render(request,"archives/familymember_add.html",{"form":form,'title':'添加家庭成员'})

# 家庭数据编辑
def familymember_edit(request,nid):
    row_obj = FamilyMember.objects.filter(id=nid).first()
    if request.method == "GET":
        form = familymember_form.familymember_add_form(instance=row_obj)
        return render(request,"archives/familymember_add.html",{"form":form,'title':'编辑家庭成员信息'})
    
    form = familymember_form.familymember_add_form(data=request.POST,instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/familymember/list/")
    print(form.errors,"===表单校验错误")
    return render(request,"archives/familymember_add.html",{"form":form,'title':'编辑家庭成员信息'})


# 家庭成员删除
def familemember_del(request,nid):
    FamilyMember.objects.filter(id=nid).delete()
    return redirect("/familymember/list/")