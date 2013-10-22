# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
	categoria = models.CharField(max_length=50, unique=True, help_text='Nombre de la categoría', verbose_name=u'Categoría')
	descripcion = models.TextField(help_text='Descripción de la categoría', verbose_name=u'Descripción')

	def __unicode__(self):
		return self.categoria

class SubCategoria(models.Model):
	subcategoria = models.CharField(max_length=50, help_text='Nombre de la subcategoría', verbose_name=u'Sub-categoría')
	categoria = models.ForeignKey(Categoria, help_text='Define la categoría para una subcategoría', verbose_name=u'Categoría')
	def __unicode__(self):
		return self.subcategoria

class Producto(models.Model):
	codigo = models.BigIntegerField(primary_key=True, help_text='Código del producto', verbose_name=u'Código')
	descripcion = models.TextField(help_text='Descripción del producto', verbose_name=u'Descripción')
	existencia = models.IntegerField(help_text='Cantidad de unidades en existencia del producto', verbose_name=u'Existencia')
	precio = models.DecimalField(max_digits=10, decimal_places=2, help_text='Precio unitario del producto', verbose_name=u'Precio')
	subcategoria = models.ForeignKey(SubCategoria, help_text='Sub-categoría del producto', verbose_name=u'Sub-categoría')
	destacado = models.BooleanField(help_text='Describe si el producto es destacado', verbose_name=u'Destacado')
	oferta = models.BooleanField(help_text='Describe si el producto esta en oferta', verbose_name=u'Oferta')
	
	def __unicode__(self):
		return self.nombre

class Orden(models.Model):
	num_orden = models.BigIntegerField(help_text='Número de Orden')
	fecha = models.DateField(auto_now=True)
	usuario = models.ForeignKey(User)
