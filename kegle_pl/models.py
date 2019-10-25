# TODO: tom/tom@kegle.pl/tom12345
from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings 
from django.utils import timezone
import datetime
from django.urls import reverse
# from django import forms
# TODO: importy do aktywacji w razie potrzeby
# import os
# from django.conf import settings

def zawody_directory_path(instance, filename):
    """ Ścieżka dla plików staycznych do zawodów.
    Pliki będą ładowane do MEDIA_ROOT/zawody/<slug>/<filename>"""
    
    return 'zawody/{0}/{1}'.format(instance.slug, filename)

def dokumenty_directory_path(instance, filename):
    """ Ścieżka dla plików programów i przepisów 
    Pliki będą ładowane do MEDIA_ROOT/<rodzaj>/<rok>/<filename>"""
    
    if isinstance(instance, Przepisy):
        return 'przepisy/{0}/{1}'.format(datetime.datetime.now().strftime ("%Y"), filename)
    if isinstance(instance, Programy):
        return 'programy/{0}/{1}'.format(datetime.datetime.now().strftime ("%Y"), filename)

class Kraje(models.Model):
    nazwa_kraju = models.CharField(max_length=250,help_text='nazwa kraju')
    kod_kraju = models.CharField(max_length=5,help_text='kod kraju')
    flaga_img = models.ImageField(upload_to='flagi/',null=True)
    nazwa_kraju_uk = models.CharField(max_length=250,help_text='nazwa kraju po angielsku')
    
    class Meta:
        db_table = 'n_kraje'
        verbose_name_plural = "Kraje"
    
    def __str__(self):
        return self.nazwa_kraju  

class Instytucje(models.Model):
    """ Instytucje - Organizator zawodów, Klub, Federacja, Reklamodawca -
    np. skelp internetowy. """
    
    RODZAJ_INSTYTUCJI = (
    (1, 'organizator'),
    (2, 'klub'),
    (3, 'federacja'),
    (4, 'reklamodawca'),
    )
    rodzaj_instytucji = models.PositiveIntegerField(choices=RODZAJ_INSTYTUCJI, help_text='Rodzaj instytucji')
    nazwa_instytucji = models.CharField(max_length=255, help_text='Nazwa instytucji')
    adres_instytucji = models.CharField(max_length=255, help_text='Adres pocztowy intytucji', blank=True)
    kraj_instytucji = models.ForeignKey(Kraje, on_delete=models.CASCADE, related_name='KrajInstytucji')
    aktywna = models.BooleanField(default=False, help_text='czy aktywna?')
    
    class Meta:
        db_table = 'n_instytucje'
        verbose_name_plural = "Instytucje"
        
    def __str__(self):
        return self.nazwa_instytucji

class UserInstytucji(models.Model):
    """ Tabela userów przypisanych do instytucji raz z uprawnieniami. """
    
    UPRAWNIENIA = (
    ('p', 'Przegląd'),
    ('e', 'Edycja'),
    ('a', 'Admin'),
    ('s','Superwisor'),
    )
    instytucje_usera = models.ManyToManyField(Instytucje, related_name='UserInstytucjiRelacja')
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    uprawnienia = models.CharField(max_length=1,choices=UPRAWNIENIA, help_text='Rola w instytucji')
    
    class Meta:
        db_table = 'n_user_instytucji'
        verbose_name_plural = "User Instytucji"

    def __str__(self): #iteruje po wszystkich nazwach z klucza many to many
        return '/n'.join([str(instytucje_usera) for instytucje_usera in self.instytucje_usera.all()])

class Wpisy(models.Model):
    """ Wpis podstawowa jednostka na portalu. Wpisem może być Artykół - strona 
    z jakimś tekstem dotyczącym userów, Zawody - zestaw informacji dotycząca 
    zawodów, Reklama. Dokument - wpis kierujący do dokumentu w formacie pdf. """
    
    WYBOR_STATUSU = (
    ('r', 'Roboczy'),
    ('o', 'Opublikowny'),
    ('a', 'Archiwalny'),
    )
    WYBOR_KATEGORII = (
    ('art', 'Artykuł'),
    ('zawody', 'Zawody'),
    ('reklama', 'Reklama'),
    ('doc', 'Dokument'),
    )
    tytul = models.CharField(max_length=250, help_text='Skrótowy tyuł wpisu')
    slug = models.SlugField(max_length=250, unique_for_date='opublikowany')
    opublikowany = models.DateTimeField(default=timezone.now)
    poprawiony = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=WYBOR_STATUSU, default='r', help_text='status wpisu')
    kategoria = models.CharField(max_length=10, choices=WYBOR_KATEGORII, default='doc' )
    dla_grupy = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='DlaGrupy')
    
    class Meta:
        db_table = 'n_wpisy'
        verbose_name_plural = "Wpisy"
        ordering = ('-opublikowany',)
    
    def __str__(self):
        return self.tytul

class Przepisy(Wpisy):
    """ Przepisy wpis typu doc, kopiowane do katalogu /przepisy/ z podziałem na 
    lata dodania. Pliki format PDF. """

    opis_tresci = models.CharField(max_length=250, null=True, help_text='Skrótowo co zawiera treść przepisu/programu')
    obowiazuje_od = models.DateField(help_text='Początek obowiązywania')
    path_plik = models.FileField(upload_to=dokumenty_directory_path)
    
    class Meta:
        db_table = 'n_przepisy'
        verbose_name_plural = "Przepisy"
        ordering = ('-obowiazuje_od',)
    
    def __str__(self):
        return '%s'' obowiązuje od ' '%s' % (self.tytul, self.obowiazuje_od)

class Programy(Wpisy):
    """ Programy wpis typu doc, kopiowane do katalogu /programy/ z podziałem na 
    lata dodania. Pliki format PDF. """
    
    opis_tresci = models.CharField(max_length=250, null=True, help_text='Skrótowo co zawiera treść przepisu/programu')
    obowiazuje_od = models.DateField(help_text='Początek obowiązywania')
    data_zmiany = models.DateField(null=True, help_text='Data zmiany wpisu')
    plik_opis = models.FileField(upload_to=dokumenty_directory_path, help_text='Plik opisu plus ew rys')
    
    class Meta:
        db_table = 'n_programy'
        verbose_name_plural = "Programy"
        ordering = ('-obowiazuje_od',)
    
    def __str__(self):
        return '%s'' obowiązuje od ' '%s' % (self.tytul, self.obowiazuje_od)

class Artykuly(Wpisy):
    """ Artykuł dziedziczy pola wpisu i dodaje swoje. Można ustawić czy jest na 
    głównej  """
    
    tresc_artykulu = models.TextField('Treść artykułu', help_text='treść artykułu')
    aktualny_do = models.DateTimeField('Do daty', blank=True, null=True, help_text=' po aktualny_do_daty nie ma być widzoczny')
    kolejnosc_artykulu = models.PositiveIntegerField(default='0', help_text='wymuszenie kolejości artykułów')
    na_glownej = models.BooleanField(default=False, help_text='czy ma być umieszczony na stronie głównej')
    
    class Meta:
        db_table = 'n_artykuly'
        verbose_name_plural = "Artykuły"

    def __str__(self):
        nazwa_z_wpisu = Wpisy.objects.get(pk=self.pk)
        return '%s'  'kolejnosc  ' '%s' % (nazwa_z_wpisu.tytul, self.kolejnosc_artykulu)

class Klasy(models.Model):
    """ Klasy sportowe w powożeniu. Podział na kategorie i rodzaje. Opłata 
    antydopingowa, należy rozumiec w następujący sposób zawody krajowe kwota
    ilość koni + zpas razy kwota w zł/eu, zawody międzynarodowe kwota w frankach
    stała od zaprzęgu. """
    
    KATEGORIA = (
    (1,'single'),
    (2,'pary'),
    (4,'czwórki'),
    )
    RODZAJ_KLASY = (
    (1, 'krajowa'),
    (2, 'miedzynarodowa'),
    (3, 'amatorskia'),
    )
    nazwa_klasy = models.CharField(max_length=55, help_text = 'np. L-1 ')
    kategoria_klasy = models.PositiveIntegerField(choices=KATEGORIA, help_text='startująca ilosc konii c-2 -> 2')
    rodzaj_klasy = models.PositiveIntegerField(choices=RODZAJ_KLASY, help_text='wybor rodzaju klasy ')
    oplata_antydopingowa = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    opis_klasy = models.CharField(max_length=255, blank=True, null=True)
    poprawiono = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'n_klasy'
        verbose_name_plural = "Klasy"
        ordering = ('rodzaj_klasy',)
        
    def __str__(self):
        return '%s'' - ''%s' %(self.nazwa_klasy, self.opis_klasy)

class RodzajeKonkursow(models.Model):
    """Rodzaj konkursów odbywające się na zawodach np. Krajowe, Międzynarodowe, 
    Amatorskie. Musi być wybrany choiaż jeden"""
    
    nazwa_rodazju_konkursu = models.CharField(max_length=300, help_text='nazwa używana na wszystkich dok. oficjalnych')

    class Meta:
        db_table = 'n_rodzaje_konkursu'
        verbose_name_plural = "Rodzaje"
    
    def __str__(self):
        return self.nazwa_rodazju_konkursu

class Zawody(Wpisy):
    """ Status zawodów otawrte można się zgłaszać, zamknięte brak 
        możliwosci edycji, odbywające_sie trwające, zablokowoand dla zgl.
        nie można się dopisywać, można wpisywać wyniki pliki itp. """
        
    STATUSU_ZAWODOW = (
    (1, 'otwarte_dla_zgl'),
    (2, 'zablokowane_dla_zgl'),
    (3, 'odbywajace_sie'),
    )
    
    oficjalna_nazwa = models.CharField(max_length=300, help_text='nazwa używana na wszystkich dok. oficjalnych')
    organizator = models.ForeignKey(Instytucje, on_delete=models.CASCADE, help_text='instytucja organizująca zawody')
    data_rozpoczecia = models.DateField()
    data_zakonczenia = models.DateField()
    rodzaje_konkursow = models.ManyToManyField(RodzajeKonkursow, related_name='RodzajeKonkursowRelacja')
    status_zawodow = models.PositiveIntegerField(choices=STATUSU_ZAWODOW, default=1, help_text='status zawodów')
    ilosc_zgloszen = models.IntegerField(blank=True, null=True, help_text='Maxymalna ilość zgłoszeń. null bez ogr.')
    miejsce_rogrywania = models.CharField(max_length=255, blank=True, null=True)
    logo_zawodow = models.ImageField(upload_to=zawody_directory_path, blank=True, null=True)
    propozycje_plik = models.FileField(upload_to=zawody_directory_path, blank=True, null=True)
    
    class Meta:
        db_table = 'n_zawody'
        verbose_name_plural = "Zawody"
        ordering = ('data_rozpoczecia',)
    
    def __str__(self):
        return self.oficjalna_nazwa
    
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName. """
        return reverse('lista_zawodow', args=[str(self.id)])

class ZawodyKomunikaty(models.Model):
    """ Komunikaty dotyczące zawodów. Docelowo możliwość  dodania/kasowania/edycji 
    przez organizatora. """
    
    zawody_id = models.ForeignKey(Zawody, on_delete=models.CASCADE)
    tytul_komunikatu = models.CharField(max_length=255, help_text='krótki tytuł komunikatu')
    komunikat = models.TextField('Treść komunikatu', help_text='treść Komunikatu do Zawodów')
    data_czas_komunikatu = models.DateTimeField(default=timezone.now)
    #TODO: może zrobić tylko zawsze i do rozpoczęcia zawodów??
    aktywny_do = models.DateTimeField(blank=True, null=True, help_text='data po której ma być nie widoczny, puste oznacza zawsze')
    kolejnosc_komuniakatu = models.PositiveIntegerField(default=0, help_text='wymuszenie kolejości komunikatów')
    del_komunikat = models.BooleanField(default = False)
    
    class Meta:
        db_table = 'n_zawody_komunikaty'
        verbose_name_plural = "Komunikaty"
    
    def __str__(self):
        return str(self.zawody_id)

class Oplaty(models.Model):
    """Opłaty zestaw. Opłaty definowane są każdorazowo na nowo dla zawodów """
    
    WALUTA = (
    ('zl','złoty'),
    ('eur','euro'),
    )
    zawody = models.ForeignKey(Zawody, on_delete=models.CASCADE, related_name='ZawodyOplaty')
    nazwa_oplaty = models.CharField(max_length=150, help_text='Nazwa opłaty')
    waluta = models.CharField(max_length=5,choices=WALUTA, help_text='Waluta opłat')
    wpisowe = models.DecimalField(max_digits=6, decimal_places=2, default = 0, \
                                  help_text='główne wpisowe jeśli brak wpisz 0')
    wpisowe_2 = models.DecimalField(max_digits=6, decimal_places=2, default = 0,\
                                     help_text='wpisowe dla dalszych par')
    boks_cena = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    trociny_cena = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,help_text='Cena za jednostkę') 
    wywoz_gowna = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,help_text='Cena za jednostkkę')
    energia_koniowoz_cena = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    energia_bus_cena = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    poprawiono = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'n_oplaty'
        verbose_name_plural = "Opłaty"
    
    def __str__(self):
#         return str(self.nazwa_oplaty) #póżniej napisać kod czytający również tytuł zawodów
        return '%s'' ' '%s' % (self.nazwa_oplaty, self.zawody.tytul)

class Konkursy(models.Model):
    """ Konkursy odbywające się na poszczególnych zawodach. Konkursy "maja"
    zawody, klasy, opłaty. Podczas Zawodów odbywają się konkursy w klasach 
    z właściwymi opłatami. Różne konkursy mogą mieć takie same opłaty. """
    
    kod_konkursu = models.CharField(max_length=25, blank=True, null=True) #zapisywany treegerem w bazie
    zawody = models.ForeignKey(Zawody, on_delete=models.CASCADE, related_name='KonkursyZawody')
    klasa = models.ForeignKey(Klasy, on_delete=models.CASCADE, related_name='KonkursyKlasy')
    oplata = models.ForeignKey(Oplaty, on_delete=models.CASCADE, related_name='KonkursyOplaty')
    poptawiono = models.DateTimeField(auto_now=True)
    nagroda_1 = models.CharField(max_length=255, blank=True, null=True)
    nagroda_3 = models.CharField(max_length=255, blank=True, null=True)
    nagroda_2 = models.CharField(max_length=255, blank=True, null=True)
    nagroda_4 = models.CharField(max_length=255, blank=True, null=True)
    nagroda_5 = models.CharField(max_length=255, blank=True, null=True)
    nagroda_6 = models.CharField(max_length=255, blank=True, null=True)
    nagroda_7 = models.CharField(max_length=255, blank=True, null=True)
    nagroda_8 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'n_konkursy'
        verbose_name_plural = "Konkursy"
        
    def __str__(self):
        return '%s' %(self.klasa)
    
class Zawodnicy(models.Model):
    """Dane zawodnika """
    
    instytucja_zawodnika = models.ForeignKey(Instytucje, on_delete=models.CASCADE, \
                                             blank=True, null=True, related_name='ZawodnikInstytucje')
    zawodnik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
                                        blank=True, null=True, related_name='ZawodnikID')                 
    imie = models.CharField(max_length=255)
    nazwisko = models.CharField(max_length=255)
    data_urodzenia = models.DateField()
    nr_pzj = models.CharField(max_length=255, blank=True, null=True)
    fei_id = models.CharField(max_length=255, blank=True, null=True)
    nazwa_klubu = models.CharField(max_length=255, blank=True, null=True)
    e_mail = models.EmailField(max_length=254, blank=True, null=True)
    telefon = models.CharField(max_length=255, blank=True, null=True)
    kraj_zawodnika = models.ForeignKey(Kraje, on_delete=models.CASCADE, related_name='KrajZawodnika')
    edycja_danych = models.BooleanField(default=False, help_text='Otworzyć do edycji zaznaczone NIE(0), odznaczone TAK(1)')
    del_zawodnika = models.BooleanField(default=False, help_text='Kasować zawodnika zaznaczone NIE (0), odznaczone TAK(1)')
    
    class Meta:
        db_table = 'n_zawodnik'
        verbose_name_plural = "Zawodnicy"
    
    def __str__(self):
        return '%s'' ' '%s' % (self.nazwisko, self.imie)

class Konie(models.Model):
    """ Koń jaki jest kazdy widzi """
    
    WYBOR_PLEC = (
    (1,'ogier'),
    (2,'klacz'),
    (3,'wałach'),
    )
    WYBOR_RODZAJ_KONIA = (
    (1,'duży koń'),
    (2,'mały koń/pony'),
    (3,'kuc'),
    )
    poprawiony = models.DateTimeField(auto_now=True)
    nazwa_konia = models.CharField('nazwa_konia',max_length=255,  help_text='nazwa123')
    rasa = models.CharField(max_length=255, blank=True, null=True, help_text='Rasa konia',)
    plec = models.PositiveIntegerField(choices=WYBOR_PLEC, help_text='Płeć konia')
    masc = models.CharField(max_length=255, blank=True, null=True)
    rodzaj = models.PositiveIntegerField(choices=WYBOR_RODZAJ_KONIA, help_text='Rodzaj konia')
    data_urodzenia_konia = models.DateField()
    ojciec = models.CharField(max_length=255, help_text='Nazwa ojca konia',null=True)
    matka = models.CharField(max_length=255,  help_text='Nazwa matki konia',null=True)
    ojciec_matki = models.CharField(max_length=255, help_text='Nazwa ojca matki konia',null=True)
    wlasciciel = models.CharField(max_length=255, help_text='Właściciel konia',null=True)
    hodowca_konia = models.CharField(max_length=255, help_text='Hodowca konia',null=True)
    nr_pzj = models.CharField(max_length=255, blank=True, null=True)
    nr_chipa_konia = models.CharField(max_length=255, blank=True, null=True)
    fei_id_konia = models.CharField(max_length=255, blank=True, null=True)
    nr_paszportu_pzj = models.CharField(max_length=255, blank=True, null=True)
    nr_paszportu_fei = models.CharField(max_length=255, blank=True, null=True)
    nr_paszportu_pzhk = models.CharField(max_length=255, help_text='Nr paszportu PZHK',null=True)
    #instytucja będąca właścicielem konia
    instytucja_konia = models.ForeignKey(Instytucje, on_delete=models.CASCADE, blank=True, null=True, related_name='KonInstytucje')
    zawodnik_konia = models.ForeignKey(Zawodnicy, on_delete=models.CASCADE,blank=True, null=True, related_name='KonZawodnik')
    kasowac_zapis_konia = models.BooleanField(default=False, help_text='Kasować konia odznaczone NIE (kasaować) , zaznaczone TAK (kasować)')
    kraj_urodzenia_konia = models.ForeignKey(Kraje, on_delete=models.CASCADE, related_name='KrajUrodzeniaKonia')

    class Meta:
        db_table = 'n_konie'
        verbose_name_plural = "Konie"

    def __str__(self):
        return '%s' %(self.nazwa_konia)

class Zgloszenia(models.Model):
    """Zgłoszenia do zawodów z nich będzie generowana lista na przegląd
    i dalej lista startujących zawodników w zawodach wraz z końmi. Pole 
    zamowienia_indeks do sprawdzenia czy idea ma sens jeśli tak to tabela 
    Zamówienia moze zniknąć. """
    
    WYBOR_STATUSU_ZGLOSZENIA = (
    ('z','zatwierdzone'),
    ('o','oczekujące'),
    ('c','czeka na płatność'),
    ('u','uzupełnić dane'),
    )
    utworzone = models.DateTimeField(default=timezone.now)
    poprawiony = models.DateTimeField(auto_now=True)
    zglaszajacy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ZglaszajacyDoZawodow')
    konkurs = models.ForeignKey(Konkursy, on_delete=models.CASCADE, related_name='ZgloszeniaKonkursy')
    zawodnik = models.ForeignKey(Zawodnicy, on_delete=models.CASCADE, related_name='ZgloszeniaZawodnik',null=True)
    notka = models.TextField(blank=True, null=True)
    status_zgloszenia = models.CharField(max_length=1,choices=WYBOR_STATUSU_ZGLOSZENIA, default = "o", help_text='ststus zgłoszenia')
    zaplacil = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    del_zgloszenie = models.BooleanField(default=False, help_text='Kasować zgłoszenie zaznaczone NIE (0), odznaczone TAK(1)')
#     zamowienia_index = models.CharField(max_length=250, help_text='2/3/1/0 co oznaczało by zgodnie z tabela Opłat poszczególne kolumny')

    class Meta:
        db_table = 'n_zgloszenia'
        verbose_name_plural = "Zgłoszenia"
        
    def __str__(self): #napisać kod pokazujący instytucje i zawodnika
        return '%s'' (''%s'')' %(self.konkurs, self.utworzone.strftime('%m/%d/%Y'))
    
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('lista_zgloszen', args=[str(self.id)])

class ZgloszoneKonie(models.Model): # lista koni zgłoszona do zawodów
    utworzone = models.DateTimeField(default=timezone.now)
    poptawiono = models.DateTimeField(auto_now=True)
    kon = models.ForeignKey(Konie, on_delete=models.CASCADE, related_name='ZgloszeneKonieLista')
    zgloszenie = models.ForeignKey(Zgloszenia, on_delete=models.CASCADE, related_name='ZgloszeneKonieZgloszenia')
    nr_konia = models.CharField(max_length=100, help_text = 'indywidualny nr konia związany z zawodami np nr zgłoszenia+A, B, C, D itd')
    przeglad = models.BooleanField(default=False, help_text='zaznaczone NIE (0), odznaczone TAK(1)')
    
    class Meta:
        db_table = 'n_zgloszone_konie'
    
    def __str__(self):
        return str(self.kon)
    
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('lista_zglosznych_koni', args=[str(self.id)])










