from django.db import models

# Create your models here.
# 用户信息
class User(models.Model):
    username = models.CharField(verbose_name='用户账号', max_length=30)
    password = models.CharField(verbose_name='用户密码', max_length=40)
    employee = models.ForeignKey(to="app01.Employee", on_delete=models.CASCADE, verbose_name='员工ID', null=True)
    avatarUrl = models.CharField(verbose_name="头像", max_length=250, null=True, blank=True)
    role = models.ForeignKey(to="Role", to_field="id", on_delete=models.SET_NULL, verbose_name='角色', null=True)
    last_login = models.DateTimeField(verbose_name='最后登录时间', auto_now=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    class Meta:
        db_table = 'sys_user'
    
# 角色
class Role(models.Model):
    name = models.CharField(verbose_name='角色名称', max_length=50)
    remark = models.CharField(verbose_name='备注', max_length=255, null=True, blank=True, )
    class Meta:
        db_table = 'sys_role'
    def __str__(self):
        return self.name
