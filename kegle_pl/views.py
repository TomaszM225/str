from django.shortcuts import render
from django.http import HttpResponse
from kegle_pl.models import Artykul, Zawody, Przepisy, Programy, ZawodyKomunikaty


def index(request): #Widok strony głównej
    """Strona główna generuje ogłoszenia ze statusem wszyscy i
    listę linków do zawodów ze statusem 1 - otwarte_dla_zgl , 2-zablokowane_dla_zgl, 3- odbywajace_sie"""
    artykuly_glowna = Artykul.objects.filter(na_glownej=1).filter(status='o').order_by('opublikowany')
    zawody_rozgrywane = Zawody.objects.filter(status_zawodow=3).filter(status='o').order_by('data_rozpoczecia')
    zawody_otwarte = Zawody.objects.filter(status='o').exclude(status_zawodow=3).order_by('data_rozpoczecia')
    context = {
        'artykuly_wszyscy':artykuly_glowna,
        'zawody_rozgrywane':zawody_rozgrywane,
        'zawody_otwarte':zawody_otwarte,
    }
    return render(request, 'kegle_pl/index.html', context=context)

def przepisy(request):
    """Lisata Przepisów i Programów"""
    przepisy = Przepisy.objects.filter(status='o')
   
    context = {
        'przepisy':przepisy,
    }
    return render(request, 'kegle_pl/przepisy.html', context=context)

def programy(request):
    """Lisata Przepisów i Programów"""
    programy = Programy.objects.filter(status='o')
    context = {
        'programy':programy,
    }
    return render(request, 'kegle_pl/programy.html', context=context)


# def przepisy_detail(request, pk): 
#     """Widok do obsługi linków otwierającyhc pdf`a przepisów"""
#     plik = get_object_or_404(PrzepisyProgramy, pk=pk)
#     pdf_data=plik.path_plik.open(mode='rb')
#     return HttpResponse(pdf_data, content_type = "application/pdf")