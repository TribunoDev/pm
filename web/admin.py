#-*- coding:utf-8 -*-
from web.models import *
from django.contrib import admin
from django import forms
admin.autodiscover()

class DetalleImgForm(forms.ModelForm):
	Producto = forms.ModelChoiceField(queryset=Producto.objects.order_by('Descripcion'))
	class Meta:
		model = Detalle_Imagen

class DetalleImgAdmin(admin.ModelAdmin):
	form = DetalleImgForm


class ProductoAdmin(admin.ModelAdmin):
	search_fields = ['Descripcion', 'Codigo']
	ordering = ['Descripcion']
	list_display = ('Descripcion','Comentarios', 'Codigo')

class Editor(admin.ModelAdmin):
	class Media:
		js = ('/home3/bufeteg1/public_html/pm.hn/pm/web/static/js/tiny_mce/tiny_mce.js', '/home3/bufeteg1/public_html/pm.hn/pm/web/static/js/editores/textareas.js')

admin.site.register(Producto, Editor)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Orden)
admin.site.register(Estado)
admin.site.register(Carrito)
admin.site.register(Detalle_Carrito)
admin.site.register(Direccion_Orden)
admin.site.register(Pais)
admin.site.register(Region)
admin.site.register(Marca)
admin.site.register(Detalle_Perfil)
admin.site.register(Detalle_Imagen, DetalleImgAdmin)
admin.site.register(Servicio_Flete)
admin.site.register(Precio_Combustible)
admin.site.register(Orden_Estado)
admin.site.register(Credito)
admin.site.register(Pagos)
admin.site.register(Ciudad)
admin.site.register(Contactos)
admin.site.register(FAQ, Editor)