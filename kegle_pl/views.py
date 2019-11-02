# from datetime import datetime 
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from kegle_pl.models import Artykuly, Przepisy, Programy, Instytucje, Oplaty, \
        Klasy, Konkursy, Zawody,  ZawodyKomunikaty, Zgloszenia, UserInstytucji, \
        Zawodnicy
from kegle_pl.forms import KonForm, ZawodnikForm

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
    else:
        return redirect('index')

def str_404(request):
    """Błąd 404"""
    txt = "Nie znalazłem strony"
    context = {
        'txt':txt,
    }
    return render(request, 'kegle_pl/str_404.html', context=context)

def curent_user_ins(user):
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
    
    przepisy = Przepisy.objects.filter(status='o')
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
    
    programy = Programy.objects.filter(status='o')
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

@login_required
@group_required('zawodnicy')
def zawodnicy_index(request):
    """Głóna strona dla główna dla zawodników. Zawodnik """
    
    zawodnik_ = Zawodnicy.objects.get(zawodnik=request.user.pk)
    zawody_ = Zawody.objects.filter(status='o')
    zgloszenia_ = Zgloszenia.objects.filter(zawodnik=zawodnik_.pk).filter(zawody_id__in=zawody_)
    
    context = {
        'zaw':zawodnik_,
        'zgloszenia':zgloszenia_,
        'zawody':zawody_
    }
    
    return render(request, 'kegle_pl/zawodnicy_index.html', context=context)

def zawodnik_dane(request):
    """Strna z danymi zawodnika, listą koni, linkami do edycji tych danych"""
    
    form = ZawodnikForm()
    
    return render(request, 'kegle_pl/zawodnicy_dodaj.html', {'form':form})

@login_required
@group_required('klub', 'klub_admin')
#TODO: Napisać obsługę strony głównnj dla klubów
def kluby_index(request):
    """Główna strona dla klubbów obsługuje admin klubu. Ma w swpoich zasobach 
     zawodników, konie które zgłasza do wybranych zawodów na zasadzie par 
     zawodnik+lista_koni """
    
    zawodnik_ = "Zawodnik Test"
    zawody_ = "Zawody Test"
    zgloszenia_ = "Zgłoszenia Test"
    
    context = {
        'zaw':zawodnik_,
        'zgloszenia':zgloszenia_,
        'zawody':zawody_
    }
    
    return render(request, 'kegle_pl/zawodnicy_index.html', context=context)