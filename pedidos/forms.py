from django import forms
from django.forms import ModelForm 
from pedidos.models import *

class EntregaForm(ModelForm):
	class Meta:
		model = Pedido