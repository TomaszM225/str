from django import forms
from django.forms import ModelForm, Textarea, NumberInput, TextInput, Select, CheckboxInput
from django.contrib.auth.models import User
from kegle_pl.models import Konie, Zawodnicy, Zgloszenia, ZgloszoneKonie, Konkursy


class KonForm(ModelForm): #Rejestracja/Edycja konia
	class Meta:
		model = Konie
		help_texts = { 
			"nazwa_konia": None,
			"rasa": None,
			"plec": None,
			"masc":None,
			"rodzaj":None,
			"data_urodzenia_konia":None,
			"ojciec":None,
			"matka":None,
			"ojciec_matki":None,
			"wlasciciel":None,
			"hodowca_konia":None,
			"nr_pzj":None,
			"nr_chipa_konia":None,
			"fei_id_konia":None,
			"nr_paszportu_pzj":None,
			"nr_paszportu_fei":None,
			"nr_paszportu_pzhk":None,
			"kraj_urodzenia_konia":None,
			"kasowac_zapis_konia": None
		}
		labels = { #label przy polach nalezy usunąc help_text z modelu bo się równiez wyświtla
			"nazwa_konia": 			"Nazwa konia",
			"rasa": 				"rasa",
			"plec": 				"płeć",
			"masc": 				"maść",
			"rodzaj": 				"rodzaj",
			"data_urodzenia_konia":	"data urodzenia",
			"ojciec":				"nazwa ojca",
			"matka":				"nazwa matki",
			"ojciec_matki":			"nazwa ojca matki",
			"wlasciciel":			"właścicel",
			"hodowca_konia":		"hodowca",
			"nr_pzj":				"nr PZJ",
			"nr_chip_a_konia":		"nr chip`a",
			"fei_id_konia":			"FEI id",
			"nr_paszportu_pzj":		"nr paszportu PZJ",
			"nr_paszportu_fei":		"nr paszportu FEI",
			"nr_paszportu_pzhk":	"nr paszportu PZHK",
			"kraj_urodzenia_konia":	"kraj urodzenia",
			"kasowac_zapis_konia":	"kasować konia?"
		}
		fields = (
			'nazwa_konia',
			'rasa','plec',
			'masc','rodzaj',
			'data_urodzenia_konia',
			'ojciec','matka',
			'ojciec_matki',
			'wlasciciel',
			'hodowca_konia',
			'nr_pzj',
			'nr_chipa_konia',
			'fei_id_konia',
			'nr_paszportu_pzj',
			'nr_paszportu_fei',
			'nr_paszportu_pzhk',
			'kraj_urodzenia_konia',
			'kasowac_zapis_konia'
		)
		widgets = {
			'data_urodzenia_konia': forms.DateInput(attrs={'placeholder': 'rrrr-mm-dd'}),
        }

class KonEditForm(ModelForm):
	class Meta:
		model = Konie
		help_texts = { 
			"nazwa_konia": None,
			"rasa": None,
			"plec": None,
			"masc":None,
			"rodzaj":None,
			"data_urodzenia_konia":None,
			"ojciec":None,
			"matka":None,
			"ojciec_matki":None,
			"wlasciciel":None,
			"hodowca_konia":None,
			"nr_pzj":None,
			"nr_chipa_konia":None,
			"fei_id_konia":None,
			"nr_paszportu_pzj":None,
			"nr_paszportu_fei":None,
			"nr_paszportu_pzhk":None,
			"kraj_urodzenia_konia":None,
			"kasowac_zapis_konia": None
		}
		labels = { #label przy polach nalezy usunąc help_text z modelu bo się równiez wyświtla
			"nazwa_konia": 			"Nazwa konia",
			"rasa": 				"rasa",
			"plec": 				"płeć",
			"masc": 				"maść",
			"rodzaj": 				"rodzaj",
			"data_urodzenia_konia":	"data urodzenia",
			"ojciec":				"nazwa ojca",
			"matka":				"nazwa matki",
			"ojciec_matki":			"nazwa ojca matki",
			"wlasciciel":			"właścicel",
			"hodowca_konia":		"hodowca",
			"nr_pzj":				"nr PZJ",
			"nr_chip_a_konia":		"nr chip`a",
			"fei_id_konia":			"FEI id",
			"nr_paszportu_pzj":		"nr paszportu PZJ",
			"nr_paszportu_fei":		"nr paszportu FEI",
			"nr_paszportu_pzhk":	"nr paszportu PZHK",
			"kraj_urodzenia_konia":	"kraj urodzenia",
			"kasowac_zapis_konia":	"kasować konia?"
		}
		fields = (
			'nazwa_konia',
			'rasa','plec',
			'masc','rodzaj',
			'data_urodzenia_konia',
			'ojciec','matka',
			'ojciec_matki',
			'wlasciciel',
			'hodowca_konia',
			'nr_pzj',
			'nr_chipa_konia',
			'fei_id_konia',
			'nr_paszportu_pzj',
			'nr_paszportu_fei',
			'nr_paszportu_pzhk',
			'kraj_urodzenia_konia',
			'kasowac_zapis_konia'
		)
class ZawodnikForm(ModelForm):#Rejestracja/Edycja zawodnika 
	class Meta:
		
		model = Zawodnicy
		exclude = (
		'instytucja_zawodnika',
		'login_zawodnika',
		'edycja_danych',
		'del_zawodnika'
		)
		labels = {
			"instytucja_zawodnika":"instytucja_zawodnika",
			"login_zawodnika":		"login_zawodnika",
			"imie":					"Imię Zawodnika",
			"nazwisko":				"Nazwisko Zawodnika",
			"data_urodzenia":		"Data urodzenia",
			"nr_pzj":				"Nr pzj",
			"fei_id":				"FEI ID",
			"e_mail":				"e_mail",
			"telefon":				"telefon",
			"kraj_zawodnika":		"kraj_zawodnika",
			"nazwa_klubu":			"Nazwa klubu",
			"edycja_danych":		"edycja_danych",
			"del_zawodnika":		"del_zawodnika",
		}
		
		fields = (
			'imie',
			'nazwisko',
			'data_urodzenia',
			'nr_pzj',
			'fei_id',
			'e_mail',
			'telefon',
			'nazwa_klubu',
			'kraj_zawodnika',
			
		)
		widgets = {
			'data_urodzenia': forms.DateInput(attrs={'placeholder': 'rrrr-mm-dd'}),
        }


# class ZglaszaneKonieDoZawodowForm(ModelForm):
# 
# 	class Meta:
# 		model = ZgloszoneKonie
# 		exclude = (
# 		'utworzone',
# 		'poptawiono',
# 		)
# 		fields = (
# 			'nr_konia',
# 			'kon',
# 			'zgloszenie',
# 			'przeglad',
# 		)
# 		labels = {
# 			"kon":"  Koń do konkursu  "
# 		}
# 		help_texts = { #zastępuje help_text z modelu na podany Nonie = nic :)
# 			"kon":None,
# 			"status":None,
# 		}
# 
# 
# class KonkursyForm(ModelForm):
# 	class Meta:
# 		model = Konkursy
# 		exclude = (
# 			'poptawiono',
# 			'kod_konkursu',
# 		)
# 		fields = (
# 			'klasy',
# 		)
# 		labels ={
# 			"klasy":		" do konkursu  ",
# 			"poptawiono":	"None",
# 			"kod_konkursu":	"None",
# 		}
# 		help_texts ={
# 			"klasy":None,
# 			"poptawiono":None,
# 			"kod_konkursu":None,
# 		}
# 	def __init__(self, zawody=None, **kwargs):
# 		super(KonkursyForm, self).__init__(**kwargs)
# 		self.fields['klasy'].queryset = Konkursy.objects.filter(zawody=zawody)
# 
# class ZgloszenieZawodnicyForm(ModelForm):
# 	class Meta:
# 		model = Zawodnicy
# 		exclude = (
# 			'login_zawodnika',
# 			'imie',
# 			'data_urodzenia',
# 			'nr_pzj',
# 			'fei_id',
# 			'nazwa_klubu',
# 			'e_mail',
# 			'telefon',
# 			'kraj_zawodnika',
# 			'edycja_danych',
# 			'del_zawodnika',
# 		)
# 		fields = (
# 			'instytucja_zawodnika',
# 		)
# 		labels = {
# 			"nazwisko":"  Nazwisko  ",
# 			"instytucja_zawodnika":""
# 		}
# 		help_texts = { #zastępuje help_text z modelu na podany Nonie = nic :)
# 			"nazwisko":None,
# 		}
# 	def __init__(self, instytucja_zawodnika=None, **kwargs):
# 		super(ZgloszenieZawodnicyForm, self).__init__(**kwargs)
# 		self.fields['instytucja_zawodnika'].queryset = Zawodnicy.objects.filter(instytucja_zawodnika=instytucja_zawodnika)
# 
# 
# 
# class ZgloszeniaForm(ModelForm):
# 	class Meta:
# 		model = Zgloszenia
# 		exclude = (
# 			#'utworzone'
# 			'status_zgloszenia',
# 		)		
# 		
# 		fields = (
# 			'zglaszajacy',
# 			'zawody',
# 			'konkurs',
# 			'zawodnik',
# 			'notka',
# 			
# 			'zaplacil',
# 			'del_zgloszenie',
# 			'zamowienia_index',
# 		)

class ZawodnikEditForm(ModelForm):
	class Meta:
		
		model = Zawodnicy
		exclude = (
		'instytucja_zawodnika',
		'login_zawodnika',
		'edycja_danych',
		'del_zawodnika'
		)
		labels = {
			"e_mail":				"e_mail",
			"telefon":				"telefon",
			"kraj_zawodnika":		"kraj_zawodnika",
			"nazwa_klubu":			"Nazwa klubu",
			"edycja_danych":		"edycja_danych",
			"del_zawodnika":		"del_zawodnika",
		}
		
		fields = (
			'e_mail',
			'telefon',
			'nazwa_klubu',
			'kraj_zawodnika',
		)
		widgets = {
			'data_urodzenia': forms.DateInput(attrs={'placeholder': 'rrrr-mm-dd'}),
        }