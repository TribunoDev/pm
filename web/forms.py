from django import forms
from django.contrib.auth.models import User 
from django.forms import ModelForm
from web.models import *

class SignUpForm(ModelForm):
	class Meta:
		model = User 
		fields = ['username', 'password', 'email', 'first_name', 'last_name']
		widgets = {
		'password': forms.PasswordInput(),
		}

class Detalle_CarritoForm(ModelForm):
    class Meta:
        model = Detalle_Carrito
        fields = ['Producto', 'Cantidad']

class Detalle_PerfilForm(ModelForm):
    class Meta:
        model = Detalle_Perfil
    