# from datetime import datetime 
from django.shortcuts import render, get_object_or_404, get_list_or_404
# from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404 
from django.http import HttpResponse
from kegle_pl.models import Artykuly, Przepisy, Programy, Instytucje, Oplaty, Klasy, Konkursy, Zawody,  ZawodyKomunikaty


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
    return render(request, 'kegle_pl/przepisy.html', context=context)

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
    return render(request, 'kegle_pl/programy.html', context=context)

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
    # TODO: Napisac obsługę
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
    print("lista konkursów",konkursy_lista)
#     if not request.user.is_authenticated:
#         konkursy_lista = Konkursy.objects.filter(zawody = pk)
#         zgloszenia_lista = Zgloszenia.objects.filter(zawody = pk)
#         zgloszenia_lista = "To będzie skrucona lista zgłoszeń"
    context = {
               'text':text,
               'zawodyInstancja':zawodyInstancja,
               'konkursy_lista':konkursy_lista,
#                'zgloszenia_lista':zgloszenia_lista,
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
#             'konkursy_lista':konkursy_lista,
#             'zgloszenia_lista':zgloszenia_lista,
    }
    return render(request, 'kegle_pl/zawody_rozgrywane_detail.html',  context=context)