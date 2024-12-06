from django.db import models

# Create your models here.
# 部门信息
class Department(models.Model):
    name = models.CharField(max_length=100,verbose_name='部门名称')
    index = models.IntegerField(verbose_name='排序',null=True,blank=True)
    def __str__(self):
        return self.name

# 员工信息
class Employee(models.Model):
    name = models.CharField(max_length=100,verbose_name='姓名')
    depart = models.ForeignKey(to="Department", on_delete=models.CASCADE,verbose_name='部门')
    job_number = models.CharField(max_length=50,verbose_name='工号')
    gender_choices = (
        (1,'男'),
        (2,'女')
    )
    gender = models.IntegerField(choices=gender_choices,default=1,verbose_name='性别',null=True,blank=True)
    birthday = models.DateField(verbose_name='出生日期',null=True,blank=True)
    phone = models.CharField(max_length=11,verbose_name='手机号码',null=True,blank=True)
    email = models.EmailField(verbose_name='邮箱',null=True,blank=True)
    address = models.CharField(max_length=255,verbose_name='家庭住址',null=True,blank=True)
    nation = models.CharField(max_length=50,verbose_name='民族',null=True,blank=True)
    marital_choices = (
        (1,'已婚'),
        (2,'未婚')
    )
    marital = models.IntegerField(choices=marital_choices,default=2,verbose_name='婚姻状况',null=True,blank=True)
    id_number = models.CharField(max_length=18,verbose_name='身份证号',null=True,blank=True)
    hiredate = models.DateField(verbose_name='入职日期')
    rank = models.CharField(max_length=50,verbose_name='职级',null=True,blank=True)
    

# 家庭成员
class FamilyMember(models.Model):
    employee = models.ForeignKey(to="Employee", on_delete=models.CASCADE,verbose_name='员工ID')
    name = models.CharField(max_length=100,verbose_name='姓名')
    relationship_choices =(
        (1,'父子'),
        (2,'母子'),
        (3,'兄弟姐妹'),
        (4,'其他')
    )
    relationship = models.IntegerField(choices=relationship_choices,verbose_name='家人关系')
    phone = models.CharField(max_length=11,verbose_name='手机号码')
    address = models.CharField(max_length=255,verbose_name='家庭住址',null=True,blank=True)



