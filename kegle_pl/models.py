# TODO: tom/tom@kegle.pl/tom12345
from django.db import models
from django.contrib.auth.models import Group
from django.utils import timezone
import datetime
from django.urls import reverse
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
    
    return '{0}/{1}/{2}'.format(instance.rodzaj+'y', datetime.datetime.now().strftime ("%Y"), filename)

class Wpis(models.Model):
    """ Wpis podstawowa jednostka na portalu. Wpisem może być 
        Artykół - strona z jakimś tekstem dotyczącym userów,
        Ogłoszenie - info dotyczące zawodów, 
        Zawody - zestaw informacji dotycząca zawodów, 
        Reklama. Jest w formie strony www. """
    
    WYBOR_STATUSU = (
    ('r', 'Roboczy'),
    ('o', 'Opublikowny'),
    ('a', 'Archiwalny'),
    )
    WYBOR_KATEGORII = (
    ('doc', 'Dokument'),
    ('zawody', 'Zawody'),
    ('reklama', 'Reklama'),
    ('ogloszenie', 'Ogłoszenie'),
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

class Artykul(Wpis):
    """ Wpis artykuł dziedziczy pola wpisu i dodaje swoje """
    
    tresc_artykulu = models.TextField('Treść artykułu', help_text='treść artykułu')
    aktualny_do = models.DateTimeField('Do daty', blank=True, help_text=' po aktualny_do_daty nie ma być widzoczny')
    kolejnosc_artykulu = models.PositiveIntegerField(default='0', help_text='wymuszenie kolejości artykułów')
    na_glownej = models.BooleanField(default='0', help_text='czy ma być umieszczony na stronie głównej')
    
    class Meta:
        db_table = 'n_artykuly'
        verbose_name_plural = "Artykuły"

    def __str__(self):
        nazwa_z_wpisu = Wpis.objects.get(pk=self.pk)
        return str(nazwa_z_wpisu.tytul)

class Ogloszenie(Wpis):
    """ Ogłoszeni organizatora, biura zawodów, lub admina, dotyczące zawodów. """
    
    tresc_ogloszenia = models.TextField('Treść ogłoszenia', help_text='treść ogłoszenia')
    aktywne_do = models.DateTimeField(null=True)
    
    class Meta:
            db_table = 'n_ogloszenia'
            verbose_name_plural = "Ogłoszenia"

    def __str__(self):
        nazwa_z_wpisu = Wpis.objects.get(pk=self.pk)
        return str(nazwa_z_wpisu.tytul)
    
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
    adres_instytucji = models.CharField(max_length=255, help_text='Adre sintytucji', blank=True)
#     kraj_instytucji = models.ForeignKey(Kraje, on_delete=models.CASCADE, related_name='KrajInstytucji')
    status = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'n_instytucje'
        verbose_name_plural = "Instytucje"
        
    def __str__(self):
        return self.nazwa_instytucji

class Zawody(Wpis):
    """ Status zawodów otawrte można się zgłaszać, zamknięte brak 
        możliwosci edycji, odbywające_sie trwające, zablokowoand dla zgl.
        nie można się dopisywać, można wpisywać wyniki pliki itp. """
        
    STATUSU_ZAWODOW = (
    (1, 'otwarte_dla_zgl'),
    (2, 'zablokowane_dla_zgl'),
    (3, 'odbywajace_sie'),
    )
    RODZAJ_ZAWODOW = (
    (1, 'krajowe'),
    (2, 'miedzynarodowe'),
    (3, 'amatorskie'),
    (4, 'kombinowane'),
    )
    oficjalna_nazwa = models.CharField(max_length=300, help_text='nazwa używana na wszystkich dok. oficjalnych')
    organizator = models.ForeignKey(Instytucje, on_delete=models.CASCADE, help_text='instytucja organizująca zawody')
    data_rozpoczecia = models.DateField()
    data_zakonczenia = models.DateField()
    status_zawodow = models.PositiveIntegerField(choices=STATUSU_ZAWODOW, default=1, help_text='status zawodów')
    rodzaj_zawodow = models.PositiveIntegerField(choices=RODZAJ_ZAWODOW, help_text='wybor kalsy zawodów')
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
    komunikat = models.TextField('Treść komunikatu', help_text='treść Komunikatu do Zawodów')
    data_czas_komunikatu = models.DateTimeField(default=timezone.now)
    kolejnosc_komuniakatu = models.PositiveIntegerField(default='0', help_text='wymuszenie kolejości komunikatów')
    del_komunikat = models.BooleanField(default = False)
    
    class Meta:
        db_table = 'n_zawody_komunikaty'
        verbose_name_plural = "Komunikaty"
    
    def __str__(self):
        return str(self.zawody_id)

class Klasy(models.Model):
    """ Klasy sportowe w powożeniu. """
    
    RODZAJ_KLASY = (
    (1,'single'),
    (2,'pary'),
    (4,'czwórki'),
    )
    nazwa_klasy = models.CharField(max_length=255, blank=True, null=True)
    opis_klasy = models.CharField(max_length=255, blank=True, null=True)
    poptawiono = models.DateTimeField(auto_now=True)
    rodzaj_klasy = models.PositiveIntegerField(choices=RODZAJ_KLASY, help_text='startująca ilosc konii c-2 -> 2')

    class Meta:
        db_table = 'n_klasy'
        verbose_name_plural = "Klasy"
        ordering = ('nazwa_klasy',)
        
    def __str__(self):
        return self.nazwa_klasy

class Oplaty(models.Model):
    """Opłaty zestaw. Anty dopingowa nalezy rozumiec w następujący sposób
    zawody krajowe kwota od konia który przeszedł przeglą w zł/eu, zawody
    międzynarodowe kwota w frankach stała od zaprzęgu. """
    
    WALUTA = (
    ('zl','złoty'),
    ('eur','euro'),
    )
    kod_oplaty = models.CharField(max_length=150, help_text='Skrótowa nazwa/kod opłaty')
    waluta = models.CharField(max_length=5,choices=WALUTA, help_text='Waluta opłat')
    wpisowe = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text='główne wpisowe jeśli brak wpisz 0')
    wpisowe_2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text='wpisowe dla dalszych par') 
    oplata_antydopingowa = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
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
        return str(self.kod_oplaty) #póżniej napisać kod czytający również tytuł zawodów

class Konkursy(models.Model):
    """ Konkursy odbywające się na poszczególnych zawodach. Konkursy "maja"
    zawody, klasy, opłaty. Podczas Zawodów odbywają się konkursy w klasach 
    z właściwymi opłatami. Różne konkursy mogą mieć takie same opłaty. """
    
    zawody = models.ForeignKey(Zawody, on_delete=models.CASCADE, related_name='KonkursyZawody')
    klasy = models.ForeignKey(Klasy, on_delete=models.CASCADE, related_name='KonkursyKlasy')
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
        return '%s' %(self.klasy)
    
class Przepisy(Wpis):
    """ Przepisy  kopiowane do katalogu /przepisy/ z podziałem na lata dodania.
    Pliki format PDF. """

    opis_tresci = models.CharField(max_length=250, null=True, help_text='Skrótowo co zawiera treść przepisu/programu')
    obowiazuje_od = models.DateField(help_text='Początek obowiązywania')
    path_plik = models.FileField(upload_to=dokumenty_directory_path)
    
    class Meta:
        db_table = 'n_przepisy'
        verbose_name_plural = "Przepisy"
        ordering = ('-obowiazuje_od',)
    
    def __str__(self):
        return '%s''-' '%s' % (self.tytul, self.obowiazuje_od)

class Programy(Wpis):
    """ Programy  kopiowane do katalogu /programy/ z podziałem na lata dodania.
    Pliki format PDF. """

    opis_tresci = models.CharField(max_length=250, null=True, help_text='Skrótowo co zawiera treść przepisu/programu')
    klasa_id = models.ForeignKey(Klasy, on_delete=models.CASCADE, related_name='DlaKlasy')
    obowiazuje_od = models.DateField(help_text='Początek obowiązywania')
    data_zmiany = models.DateField(null=True, help_text='Data zmiany wpisu')
    plik_opis = models.FileField(upload_to=dokumenty_directory_path)
    rysunek_plik = models.FileField(upload_to=dokumenty_directory_path, null=True)
    
    class Meta:
        db_table = 'n_programy'
        verbose_name_plural = "Programy"
        ordering = ('-obowiazuje_od',)
    
    def __str__(self):
        return '%s''-' '%s' % (self.klasa_id.nazwa_klasy, self.tytul, self.obowiazuje_od)