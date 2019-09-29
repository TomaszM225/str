from django.contrib import admin
from .models import *
from django import forms
from ckeditor.widgets import CKEditorWidget
#TODO: Zainstaluj ckeditr edytor HTML polecenie pip3 install django-ckeditor 
 

#class ZawodyAdminForm(forms.ModelForm):
#     
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.initial['kategoria'] = 'zawody'
#     
#     class Meta:
#         model = Zawody
#         fields = '__all__'
#         exclude = ['kategoria']
# 
# class ZawodyAdmin(admin.ModelAdmin):
#     list_display = ('oficjalna_nazwa','status_zawodow','data_rozpoczecia','status')
#     prepopulated_fields = {'slug': ('tytul',)}
#     form = ZawodyAdminForm

class ArtykulAdminForm(forms.ModelForm):
    tresc_artykulu = forms.CharField(widget=CKEditorWidget())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['kategoria'] = 'ogloszenie'
        
    class Meta:
        model = Artykul
        fields = '__all__'
        exclude = ['kategoria']

class ArtykulAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'status', 'poprawiony')
    prepopulated_fields = {'slug': ('tytul',)}
    form = ArtykulAdminForm
    
class PrzepisyProgramyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('tytul',)}

admin.site.register(PrzepisyProgramy,PrzepisyProgramyAdmin)
admin.site.register(Artykul, ArtykulAdmin)
#admin.site.register(Zawody, ZawodyAdmin)
