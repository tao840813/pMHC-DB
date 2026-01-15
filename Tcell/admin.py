from django.contrib import admin
from Tcell.models import Epitope
# Register your models here.
#admin.site.register(Epitope)
class EpitopeAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'mhc_ambiguity', 'old_allele_name', 'mhc_convert','journal')
    list_filter = ('mhc_ambiguity',)
    search_fields = ('mhc_ambiguity', 'mhc_convert')
    ordering = ('id', 'mhc_ambiguity',)


admin.site.register(Epitope, EpitopeAdmin)

