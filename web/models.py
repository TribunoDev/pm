# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
	Categoria = models.CharField(max_length=50, unique=True, help_text='Nombre de la categoría', verbose_name=u'Categoría')
	Descripcion = models.TextField(help_text='Descripción de la categoría', verbose_name=u'Descripción')

	def __unicode__(self):
		return self.Categoria

class SubCategoria(models.Model):
	Subcategoria = models.CharField(max_length=50, help_text='Nombre de la subcategoría', verbose_name=u'Sub-categoría')
	Descripcion = models.TextField(help_text='Descripción de la Sub-categoría', verbose_name=u'Descripción')
	Categoria = models.ForeignKey(Categoria, help_text='Define la categoría para una subcategoría', verbose_name=u'Categoría')
	def __unicode__(self):
		return self.Subcategoria

class Producto(models.Model):
	Codigo = models.BigIntegerField(primary_key=True, help_text='Código del producto', verbose_name=u'Código')
	Descripcion = models.TextField(help_text='Descripción del producto', verbose_name=u'Descripción')
	Existencia = models.IntegerField(help_text='Cantidad de unidades en existencia del producto', verbose_name=u'Existencia')
	Precio = models.DecimalField(max_digits=10, decimal_places=2, help_text='Precio unitario del producto', verbose_name=u'Precio')
	Subcategoria = models.ForeignKey(SubCategoria, help_text='Sub-categoría del producto', verbose_name=u'Sub-categoría')
	Destacado = models.BooleanField(help_text='Describe si el producto es destacado', verbose_name=u'Destacado')
	Oferta = models.BooleanField(help_text='Describe si el producto esta en oferta', verbose_name=u'Oferta')
	Imagen = models.ImageField(upload_to='img_productos',verbose_name=u'Imágen')
	
	def __unicode__(self):
		return self.Descripcion

class Pais(models.Model):
	Pais = models.CharField(max_length=45, help_text='Ingrese el nombre del país', verbose_name=u'País')
	def __unicode__(self):
		return self.Pais

class Direccion_Orden(models.Model):
	Nombre = models.CharField(max_length=50, help_text='Ingrese el nombre completo del contacto', verbose_name=u'Nombre')
	Direccion = models.TextField(help_text='Ingrese la dirección para el envío', verbose_name=u'Dirección')
	Ciudad = models.CharField(max_length=50, help_text='Ingresa una ciudad para la dirección')
	Region = models.CharField(max_length=50, help_text='Ingresar una región, estado o provincia', verbose_name=u'Estado')
	Postal = models.IntegerField(help_text='Ingrese el codigo postal del pais de ubicación', verbose_name=u'Codigo Postal')
	Pais = models.ForeignKey(Pais)
	Telefono = models.IntegerField(help_text='Ingrese el teléfono de contacto', verbose_name=u'Teléfono')

	def __unicode__(self):
		return self.Direccion +' '+ self.Ciudad +', '+ self.Region +', '+ self.Pais.Pais

class Estado_Orden(models.Model):
	Estado = models.CharField(max_length=45, help_text='Describe el estado de la orden', verbose_name=u'Estado de Orden')
	def __unicode__(self):
		return self.Estado

class Orden(models.Model):
	Fecha = models.DateField(help_text='Ingresar Fecha de la orden', verbose_name=u'Fecha')
	Usuario = models.ForeignKey(User, help_text='Seleccionar el usuario', verbose_name=u'Usuario')
	Estado = models.ForeignKey(Estado_Orden, help_text='Estado de la orden de productos', )
	Direccion = models.ForeignKey(Direccion_Orden, help_text='Ingresar la dirección para el envío del producto', verbose_name=u'Dirección')

	def __unicode__(self):
		return str(self.pk)

class Detalle_Orden(models.Model):
	Orden = models.ForeignKey(Orden, help_text='Número de orden para compra en linea')
	Producto = models.ForeignKey(Producto, help_text='Código del producto seleccionado', verbose_name=u'Código de Producto')
	Cantidad = models.IntegerField(help_text='Cantidad de producto', verbose_name=u'Cantidad')

	def __unicode__(self):
		return self.Cantidad +' '+ self.Producto

class Marca(models.Model):
	Marca = models.CharField(max_length=50, help_text='Nombre de la marca', verbose_name=u'Marca')
	Logotipo = models.ImageField(upload_to='img_marcas', verbose_name=u'Logotipo')

	def __unicode__(self):
		return self.Marca
