from django.contrib import admin

# Register your models here.
from myapp.models import student

# admin.site.register(student) # 最簡易的顯示

class studentAdmin(admin.ModelAdmin):
    list_display=('id','cName','cSex','cBirthday','cEmail','cPhone',)
    list_filter=('cSex',)
    search_fields=('cName','cEmail','cPhone',)
    ordering=('id','cName',)

admin.site.register(student, studentAdmin)
