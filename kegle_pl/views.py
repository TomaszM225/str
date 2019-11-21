# from datetime import datetime 
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from kegle_pl.models import Artykuly, Przepisy, Programy, Instytucje, \
        Klasy, Konkursy, Zawody,  ZawodyKomunikaty, Zgloszenia, UserInstytucji, \
        Zawodnicy, Konie, ZgloszoneKonie, OplatyGrupy, OplatyNazwy, OplatyCeny
from kegle_pl.forms import KonForm, KonEditForm, ZawodnikForm, ZawodnikEditForm
# from django.template.context_processors import request
#from aiohttp.client import request

def group_required(*group_names): 
    """Sprawdzenie zalogowanego user`a czy jest w odpwoeidniej grupie lub superuserem."""    
    
    def in_groups(u):       
        if u.is_authenticated:            
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True        
            return False    
    return user_passes_test(in_groups)

def login_success(request): 
    """ Po zalogowaniu przeniesie usera do właściwej strony głównej
    """
    if request.user.groups.filter(name='zawodnicy').exists():
        return redirect('zawodnicy_index')
    elif request.user.groups.filter(name='klub_admin').exists():
        return redirect('kluby_index')
    elif request.user.groups.filter(name='rejestracja').exists():
        return redirect('zawodnik_dodaj')
    else:
        return redirect('index')

def str_404(request):
    """Błąd 404"""
    txt = "Nie znalazłem strony"
    context = {
        'txt':txt,
    }
    return render(request, 'kegle_pl/str_404.html', context=context)

def instytucja_usera(user):
    """wybór instytucji dla zalogowanego usera"""
    curent_user=UserInstytucji.objects.get(auth_user=user)  
    current_inst = Instytucje.objects.get(UserInstytucjiRelacja=curent_user.pk)  
    return( current_inst )

def index(request): #Widok strony głównej
    """Strona główna generuje ogłoszenia ze statusem wszyscy i listę linków do 
    zawodów ze statusem 1 - otwarte_dla_zgl , 2-zablokowane_dla_zgl, 
    3- odbywajace_sie. """
    
    artykuly_glowna = Artykuly.objects.filter(na_glownej=1).filter(status='o').order_by('kolejnosc_artykulu')  
    zawody_rozgrywane = Zawody.objects.filter(status_zawodow=3).filter(status='o').order_by('data_rozpoczecia')  
    zawody_otwarte = Zawody.objects.filter(status='o').exclude(status_zawodow=3).order_by('data_rozpoczecia')  
    context = {
        'artykuly_glowna':artykuly_glowna,
        'zawody_rozgrywane':zawody_rozgrywane,
        'zawody_otwarte':zawody_otwarte,
    }
    return render(request, 'kegle_pl/index.html', context=context)

def przepisy(request):
    """Lisata linków do przepisów ze statusem opublikowany.Linki podzielone są 
    na roczniki publikacji. Linki kierują na plik dokumentu w srtandardzie pdf. 
    """

    przepisy = get_list_or_404(Przepisy, status='o')
    context = {
        'przepisy':przepisy,
    }
    return render(request, 'kegle_pl/doc.html', context=context)

def przepisy_detail(request, pk): 
    """Widok do obsługi linków otwierającyhc pdf`a przepisów"""
    
    plik = get_object_or_404(Przepisy, slug=pk)
    pdf_data=plik.path_plik.open(mode='rb')
    return HttpResponse(pdf_data, content_type = "application/pdf")

def programy(request):
    """Lisata linków do programów ze statusem opublikowany. Linki kierują na plik 
    dokumentu w srtandardzie pdf."""
    
    programy = get_list_or_404(Programy, status='o')
    context = {
        'programy':programy,
    }
    return render(request, 'kegle_pl/doc.html', context=context)

def programy_detail(request, pk): 
    """Widok do obsługi linków otwierającyhc pdf`a przepisów"""
    
    plik = get_object_or_404(Programy, slug=pk)
    pdf_data=plik.plik_opis.open(mode='rb')
    return HttpResponse(pdf_data, content_type = "application/pdf")

def artykuly(request):
    """Lista artykułów """
    artykuly = Artykuly.objects.filter(na_glownej=0).filter(status='o')  
    context = {
        'artykuly':artykuly,
    }
    return render(request, 'kegle_pl/artykuly.html', context=context)

def arch_programow_przepisow(request):
    """ Widok programów i przepisów  w archiwum """
    # TODO: Napisac obsługę archiwum programów i przepisów
    pass

def zawody_aktywne(request):
    """Widok listy zawodów ze statusem wpisu opublikowany na stronie index.
    pogrupowane eg statusu zawodów:  'odbywajace_sie' osobna sekcja oraz
    'otwarte_dla_zgl' i 'zablokowane_dla_zgl'posortowane wg daty rozpoczęcia. """ 
    # TODO: Na stronie na telefon powinno się robić tafelki zawodów do sprawdzenia
    
    zawody_otwarte_ = get_object_or_404(Zawody, status_zawodow='o')
    zawody_rozgrywane_ = Zawody.objects.filter(status_zawodow=3).filter(status='o').order_by('data_rozpoczecia')  
    context = {
               'zawody_otwarte': zawody_otwarte_,
               'zawody_rozgrywane':zawody_rozgrywane_
    }
    return render(request, 'kegle_pl/index.html', context=context)

def zawody_aktywne_propozycje(request, pk):
    """Widok do obsługi linków otwierającyhc pdf`a propozycji"""
    
    zawody = get_object_or_404(Zawody, slug=pk)
    pdf_data=zawody.propozycje_plik.open(mode='rb')
    return HttpResponse(pdf_data, content_type = "application/pdf")

def zawody_aktywne_detail(request, pk):
    """ Widok detali dla wybranych zawodów. Sekcje: komunikat-
    treść komunikatu dla wszystkicj dotyczace tych zawodów, propozycje -
    link do propozycjj, lista zgłoszonych."""
    
    zawodyInstancja = get_object_or_404(Zawody, pk=pk)
    try:
        text = ZawodyKomunikaty.objects.filter(zawody_id=pk)  
    except ZawodyKomunikaty.DoesNotExist: 
        text = 'none'
    konkursy_lista = Konkursy.objects.filter(zawody = pk)  
    if not request.user.is_authenticated:
        konkursy_lista = Konkursy.objects.filter(zawody = pk)  
#         zgloszenia_lista = Zgloszenia.objects.filter(zawody = pk)
#         zgloszenia_lista = "To będzie skrucona lista zgłoszeń"
    context = {
               'text':text,
               'zawodyInstancja':zawodyInstancja,
               'konkursy_lista':konkursy_lista,
#                 'zgloszenia_lista':zgloszenia_lista,
    }
        
    return render(request, 'kegle_pl/zawody_aktywne_detail.html',  context=context)
    
def zawody_rozgrywane_detail(request, pk):
    """ Widok detali zawodów rogrywanych listy startowe itp"""
    
    zawodyInstancja = get_object_or_404(Zawody, pk=pk)
    try:
        text = ZawodyKomunikaty.objects.filter(zawody_id=pk)  
    except ZawodyKomunikaty.DoesNotExist:  
        text = 'none'
    context = {
               'text':text,
               'zawodyInstancja':zawodyInstancja,
#                'konkursy_lista':konkursy_lista,
#                'zgloszenia_lista':zgloszenia_lista,
    }
    return render(request, 'kegle_pl/zawody_rozgrywane_detail.html',  context=context)

@login_required()
@group_required('zawodnicy')
def zawodnicy_index(request):
    """Głóna strona dla główna dla zawodników. Wyświtla aktualne zgłoszenie
    do zawodów jako linki do edycji o ile nie zostaną zaakceptowane. """
    
    #zawodnik_ = get_object_or_404(Zawodnicy, user=request.user.pk)
    zawodnik_ = Zawodnicy.objects.get(user_id=request.user.pk)  
    zawody_ = Zawody.objects.filter(status='o')  
    zgloszenia_ = Zgloszenia.objects.filter(zawodnik=zawodnik_.pk).filter(zawody_id__in=zawody_)  
    
    context = {
               'zaw':zawodnik_,
               'zgloszenia':zgloszenia_,
               'zawody':zawody_
    }
    
    return render(request, 'kegle_pl/zawodnicy_index.html', context=context)

@login_required()
@group_required('zawodnicy')
def zawodnik_dane(request):
    """Strona zawierające dane zawodnika, listę koni. Zawirać będzie przyciski 
    dodające konia, zmianę opisu itp. """
    
    zawodnik_ = Zawodnicy.objects.get(user_id=request.user.pk)  
    
    context = {
               'post':zawodnik_,   
    }
    
    return render(request, 'kegle_pl/zawodnicy_dane.html', context=context)

@login_required()
@group_required('zawodnicy')
def zawodnik_edytuj(request):
    """Po nadaniu praw do edycji dla Zawodnika strona edycji danych zawodnika staje się aktywna"""

    zawodnik_ = Zawodnicy.objects.get(user=request.user.pk)  
    if zawodnik_.edycja_danych == 0:
        if request.method == "POST":
            zawodnik_edit_form = ZawodnikEditForm(request.POST, instance=zawodnik_)
            if zawodnik_edit_form.is_valid():
                zawodnik_edit_form = zawodnik_edit_form.save(commit=False)
                zawodnik_edit_form.save()
                return redirect('zawodnicy_index')
        else:
            zawodnik_edit_form = ZawodnikEditForm(instance=zawodnik_)
            return render(request, 'kegle_pl/zawodnicy_zmiana.html', {'zawodnik_edytuj': zawodnik_edit_form})
    else:
        zawodnik_dodaj_form = ZawodnikForm(instance=zawodnik_)
        return render(request, 'kegle_pl/zawodnicy_zmiana.html', {'zawodnik_dodaj': zawodnik_dodaj_form})
       
@login_required()
@group_required('rejestracja')
def zawodnik_dodaj(request):
    """Rejestracja zawodnika i zamiana grupy 
    *---------------------------------------------------------
    * Trzeba napisać obsługę błędu jak juz istnieje zawodnik
    *---------------------------------------------------------
    """
    if request.method == "POST":
        zawodnik_dodaj_form = ZawodnikForm(request.POST)
        if zawodnik_dodaj_form.is_valid():
            zawodnik_dodaj_form = zawodnik_dodaj_form.save(commit=False)
            zawodnik_dodaj_form.user=request.user #wpisanie id usera
            user_gr = User.groups.through.objects.get(user=request.user)
            grupa = Group.objects.get(name='zawodnicy')
            user_gr.group = grupa
            zawodnik_dodaj_form.save()
            user_gr.save()
            return redirect('zawodnicy_index')
    else:
        zawodnik_dodaj_form = ZawodnikForm()
    return render(request, 'kegle_pl/zawodnicy_zmiana.html', {'zawodnik_dodaj': zawodnik_dodaj_form})

@login_required()
@group_required('zawodnicy','klub_admin')
def konie_index(request):
    """Lista koni przypisanych do User`a. """
    
    if request.user.groups.filter(name='zawodnicy').exists():
        zawodnik = get_object_or_404(Zawodnicy, user=request.user.pk)
        kon_lista = Konie.objects.filter(user_konia=zawodnik).filter(kasowac_zapis_konia=False)  
    else:
#     if request.user.groups.filter(name='klub_admin').exists():
        print("Konie instytucji")
        instytucja=instytucja_usera(request.user.pk)
        kon_lista = Konie.objects.filter(instytucja_konia=instytucja).filter(kasowac_zapis_konia=False)  
    context = {
               'kon_lista':kon_lista,
    }
    
    return render(request, 'kegle_pl/konie_index.html', context=context)

@login_required()
@group_required('zawodnicy','klub_admin')
def kon_dane(request, pk):
    """Strona daych konia z możliwością zamiany niektórych parametrów"""

    kon_ = Konie.objects.get(pk=pk)  
    context = {
               'post': kon_,
    }
    return render(request, 'kegle_pl/kon_dane.html', context=context)

@login_required()
@group_required('zawodnicy','klub_admin')
def kon_edit(request, pk):
    kon_do_zmiany = Konie.objects.get(pk=pk)  
    if request.method == "POST":
            kon_dodaj_form = KonEditForm(request.POST, instance=kon_do_zmiany)
            if kon_dodaj_form.is_valid():
                kon_dodaj_form = kon_dodaj_form.save(commit=False)
                kon_dodaj_form.save()
                return redirect('zawodnicy_index')
    else:
        kon_dodaj_form = KonEditForm(instance=kon_do_zmiany)
        return render(request, 'kegle_pl/konie_zmiana.html', {'form': kon_dodaj_form})

@login_required()
@group_required('zawodnicy','klub_admin')
def kon_dodaj(request):
    """dodawanie nowego konia pełna informacja do wpisania"""

    if request.method == "POST":
        kon_dodaj_form = KonForm(request.POST)
        if kon_dodaj_form.is_valid():
            kon_dodaj_form = kon_dodaj_form.save(commit=False)
            if request.user.groups.filter(name='zawodnicy').exists():
                zawodnik = Zawodnicy.objects.get(user=request.user.pk)  
                kon_dodaj_form.user_konia=zawodnik
                kon_dodaj_form.save()
                return redirect('zawodnicy_index')
            if request.user.groups.filter(name='klub_admin').exists():
                instytucja=instytucja_usera(request.user.pk)
                kon_dodaj_form.instytucja_konia=instytucja
                kon_dodaj_form.save()
                return redirect('instytucje_index')
    else:
        kon_dodaj_form = KonForm()
    return render(request, 'kegle_pl/konie_zmiana.html', {'form': kon_dodaj_form}) 

@login_required()
@group_required('zawodnicy','klub_admin')
def kon_kasuj(request):
#TODO: Napisać procedurę
    """Kasowanie rekordu konia z bazy"""
    pass   


@login_required()
@group_required('klub', 'klub_admin')
def kluby_index(request):
    """Główna strona dla klubbów obsługuje admin klubu. Ma w swpoich zasobach 
     zawodników, konie które zgłasza do wybranych zawodów na zasadzie par 
     zawodnik+lista_koni """
   
    #TODO: Napisać obsługę strony głównnj dla klubów
    zawodnik_ = "Zawodnik Test"
    zawody_ = "Zawody Test"
    zgloszenia_ = "Zgłoszenia Test"
    
    context = {
               'zaw':zawodnik_,
               'zgloszenia':zgloszenia_,
               'zawody':zawody_
    }
    
    return render(request, 'kegle_pl/zawodnicy_index.html', context=context)

@login_required()
@group_required('zawodnicy','klub_admin')
def zgloszenie_dodaj(request, pk):
    """Strona ze zgłoszeiem zawodnika do zawodów indywidualnie i z klubu"""
    op = []
    zaw_ = get_object_or_404(Zawodnicy, user=request.user.pk)
    print("User ", zaw_)
    konkurs_ = Konkursy.objects.get(pk=pk)
    print("-"*20)
    print(konkurs_.zawody)
    print("Nazwa klasy",konkurs_.klasa.nazwa_klasy)
    print("Rodzaj zawodów", konkurs_.klasa.rodzaj_klasy)
    print("Ilość koni w konkursie", konkurs_.klasa.kategoria_klasy)
    print("Opłata antydopingowa", konkurs_.klasa.oplata_antydopingowa)
    print("Opłaty ", konkurs_.oplata)
    us= OplatyGrupy.objects.get(pk = konkurs_.oplata.pk)
    for oplata in us.oplata.all():
#         print('%s'%(i))
        for t in oplata.oplaty_detale.all():
            print("Dane do pobrania:" ,t.nazwa_oplaty, t.cena, t.waluta)
            di = {
                "op1":t.nazwa_oplaty, 
                "cena":t.cena, 
                "waluta":t.waluta 
                }
            op.append(di)
            
    print("Lista opłat:",op)
    if request.user.groups.filter(name='zawodnicy').exists():
        konie_ = Konie.objects.filter(user_konia=zaw_.pk)
        print("Konie zawodnika:")
    if request.user.groups.filter(name='klub_admin').exists():
        instytucja=instytucja_usera(zaw_.pk)
        konie_ = Konie.objects.filter(instytucja_konia=instytucja)
        print("Konie klubu:")
    print(konie_)
    print("-"*20)
    context = {
        'zawody':konkurs_.zawody,
        'konie':konie_,
    }
    return render(request, 'kegle_pl/zgloszenie_dodaj.html', context=context)
    
    
