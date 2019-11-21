from django.contrib import admin
from .models import Artykuly, Przepisy, Programy, Instytucje, OplatyGrupy, OplatyCeny, OplatyNazwy, \
        Klasy, Konkursy, Zawody,  ZawodyKomunikaty, Zgloszenia, UserInstytucji, \
        Zawodnicy, Konie, ZgloszoneKonie, Zamowienia
from django import forms
from ckeditor.widgets import CKEditorWidget

#TODO: Zainstaluj ckeditr edytor HTML polecenie pip3 install django-ckeditor 

class ZawodyAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#         self.initial['kategoria'] = 'zawody'
     
    class Meta:
        model = Zawody
        fields = '__all__'
        exclude = ['kategoria']
         
class ZawodyAdmin(admin.ModelAdmin):
    list_display = ('oficjalna_nazwa','status_zawodow','data_rozpoczecia','status')
    prepopulated_fields = {'slug': ('tytul',)}
    form = ZawodyAdminForm

class ArtykulAdminForm(forms.ModelForm):
    tresc_artykulu = forms.CharField(widget=CKEditorWidget())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = Artykuly
        fields = '__all__'

class ArtykulyAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'status', 'poprawiony',  'na_glownej', 'kolejnosc_artykulu')
    prepopulated_fields = {'slug': ('tytul',)}
    form = ArtykulAdminForm
    
class PrzepisyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('tytul',)}
     
class ProgramyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('tytul',)}
    
# class OplatyAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'kod_oplaty'}


class ZawodyKomunikatyAdminForm(forms.ModelForm):
    komunikat = forms.CharField(widget=CKEditorWidget())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = ZawodyKomunikaty
        fields = '__all__'

class ZawodyKomunikatyAdmin(admin.ModelAdmin):
    list_display = ('tytul_komunikatu', 'zawody_id', 'data_czas_komunikatu', 'kolejnosc_komuniakatu',  'del_komunikat')
    #prepopulated_fields = {'slug': ('tytul',)}
    form = ZawodyKomunikatyAdminForm
    
    
admin.site.register(Artykuly, ArtykulyAdmin)  # @UndefinedVariable
admin.site.register(Przepisy,PrzepisyAdmin)  # @UndefinedVariable
admin.site.register(Programy,ProgramyAdmin)  # @UndefinedVariable
admin.site.register(Zawody, ZawodyAdmin)  # @UndefinedVariable
admin.site.register(OplatyGrupy)
admin.site.register(OplatyCeny)
admin.site.register(OplatyNazwy)
admin.site.register(Instytucje)  # @UndefinedVariable
admin.site.register(UserInstytucji)  # @UndefinedVariable
admin.site.register(Konkursy)  # @UndefinedVariable
admin.site.register(Klasy)  # @UndefinedVariable
admin.site.register(ZawodyKomunikaty,ZawodyKomunikatyAdmin)  # @UndefinedVariable
admin.site.register(Zawodnicy) # @UndefinedVariable
admin.site.register(Zgloszenia)  # @UndefinedVariable
admin.site.register(ZgloszoneKonie)  # @UndefinedVariable
admin.site.register(Zamowienia)