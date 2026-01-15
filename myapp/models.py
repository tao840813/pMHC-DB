from django.db import models
from django.utils import timezone

# Create your models here.
class student(models.Model):
    SEX_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]
    cName = models.CharField('姓名',max_length=20, null=False)
    cSex = models.CharField('性別',max_length=1, choices=SEX_CHOICES, default='', null=False)
    cBirthday = models.DateField('生日',null=False)
    cEmail = models.EmailField('Email',max_length=100, blank=True, default='')
    cPhone = models.CharField('手機',max_length=50, blank=True, default='')
    cAddr = models.CharField('地址',max_length=255, blank=True, default='')
    last_modified = models.DateTimeField('最后修改日期', auto_now = True)
    created = models.DateTimeField('保存日期',default = timezone.now)

    def __str__(self):
        return self.cName
