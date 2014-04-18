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
	ordering = ['-Imagen']


class ProductoAdmin(admin.ModelAdmin):
	search_fields = ['Descripcion', 'Codigo']
	ordering = ['Descripcion']
	list_display = ('Descripcion', 'Codigo')

class SubcategoriaAdmin(admin.ModelAdmin):
	search_fields = ['CodigoSubcategoria']
	ordering = ['Subcategoria']
	list_display = ('Subcategoria','CodigoSubcategoria')

class Editor(admin.ModelAdmin):
	class Media:
		js = ('../static/js/tiny_mce/tiny_mce.js', '../static/js/editores/textareas.js')

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)
admin.site.register(SubCategoria, SubcategoriaAdmin)
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