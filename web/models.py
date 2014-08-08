#!/usr/bin/python
#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import *
from django.dispatch.dispatcher import receiver
from easy_thumbnails.files import get_thumbnailer
from django.template import defaultfilters


class Detalle_Perfil(models.Model):
	RNP=models.CharField(max_length=20, help_text='RNP del Usuario', verbose_name=u'RNP')
	Direccion = models.CharField(max_length=250, help_text='Direccion residencial del usuario', verbose_name=u'Direccion', null=True, blank=True)
	Telefono = models.CharField(max_length=10, null=True, blank=True, help_text='Teléfono del usuario', verbose_name=u'Telefono')
	Usuario = models.ForeignKey(User, unique=True, help_text='Usuario al que pertenece la dirección', verbose_name=u'Usuario')
	class Meta:
		verbose_name_plural=u'Detalle del perfil del usuario'
	def __unicode__(self):
		return self.Usuario.username

class Categoria(models.Model):
	CodigoCategoria = models.CharField(max_length=25)
	Categoria = models.CharField(max_length=50, unique=True, help_text='Nombre de la categoría', verbose_name=u'Categoría')
	class Meta:
		verbose_name_plural=u'Categoría para el producto'
	def __unicode__(self):
		return self.Categoria

class SubCategoria(models.Model):
	CodigoSubcategoria = models.CharField(max_length=25)
	Subcategoria = models.CharField(max_length=50, help_text='Nombre de la subcategoría', verbose_name=u'Sub-categoría')
	Categoria = models.ForeignKey(Categoria, help_text='Define la categoría para una subcategoría', verbose_name=u'Categoría')
	class Meta:
		verbose_name_plural=u'Subcategoría para producto'
	def __unicode__(self):
		return self.Subcategoria



class Producto(models.Model):
	Codigo = models.CharField(max_length=100, primary_key=True, help_text='Código del producto', verbose_name=u'Código')
	#idProductoMonica = models.IntegerField(null=True, blank=True)
	Descripcion = models.CharField(max_length=200, help_text='Descripción del producto', verbose_name=u'Descripción')
	Existencia = models.IntegerField(help_text='Cantidad de unidades en existencia del producto', verbose_name=u'Existencia')
	Precio = models.DecimalField(max_digits=10, decimal_places=2, help_text='Precio unitario del producto', verbose_name=u'Precio')
	Subcategoria = models.ForeignKey(SubCategoria, help_text='Sub-categoría del producto', verbose_name=u'Sub-categoría')
	Destacado = models.BooleanField(help_text='Describe si el producto es destacado', verbose_name=u'Destacado')
	Oferta = models.BooleanField(help_text='Describe si el producto esta en oferta', verbose_name=u'Oferta')
	Fecha = models.DateField(auto_now_add=True, blank=True, null=True)
	Comentarios=models.TextField(help_text='Ingrese especificaciones del producto', verbose_name=u'Comentarios')
	Notas=models.CharField(max_length=200, help_text='Ingrese la marca del producto', verbose_name=u'Notas')
	Activo=models.BooleanField(verbose_name=u'Activo')
	class Meta:
		verbose_name_plural=u'Producto'
	def __unicode__(self):
		return self.Descripcion
@receiver(post_save, sender=Producto)
def delete_old_ReporteOferta(sender, instance, **kwargs):
	if ReporteOfertaDestacado.objects.filter(Producto=instance).count() > 0:
		hist = ReporteOfertaDestacado.objects.get(Producto=instance)
		hist.delete()
		print "Registro eliminado"
	historial = ReporteOfertaDestacado(Producto = instance)
	if instance.Oferta and instance.Destacado:
		historial.save()
	elif instance.Oferta and instance.Destacado == False:
		historial.save()
	elif instance.Oferta == False and instance.Destacado:
		historial.save()

class Imagen(models.Model):
	Producto = models.OneToOneField(Producto)
	Imagen = models.ImageField(upload_to='thumbnail', verbose_name=u'Imagen del Producto')
	class Meta:
		verbose_name_plural=u'Imagen para producto'
	def __unicode__(self):
		return self.Producto.Descripcion
@receiver(pre_delete, sender=Imagen)
def Imagen_delete(sender, instance, **kwargs):
	instance.Imagen.delete(False)

@receiver(pre_save, sender=Imagen)
def delete_old_Imagen(sender, instance, *args, **kwargs):
	if instance.pk:
		existing_Imagen = Imagen.objects.get(pk=instance.pk)
		if instance.Imagen and existing_Imagen.Imagen != instance.Imagen:
			existing_Imagen.Imagen.delete(False)

class Detalle_Imagen(models.Model):
	Producto = models.ForeignKey(Imagen)
	Imagen = models.ImageField(upload_to='img_detalle')
	class Meta:
		verbose_name_plural=u'Imagenes del Producto'
	def __unicode__(self):
		return str(self.Imagen)

@receiver(pre_delete, sender=Detalle_Imagen)
def Detalle_Imagen_delete(sender, instance, **kwargs):
	instance.Imagen.delete(False)

@receiver(pre_save, sender=Detalle_Imagen)
def delete_old_Detalle_Imagen(sender, instance, *args, **kwargs):
	if instance.pk:
		existing_Imagen = Detalle_Imagen.objects.get(pk=instance.pk)
		if instance.Imagen and existing_Imagen.Imagen != instance.Imagen:
			easy_thumbnails.delete_thumbnails(existing_Imagen.Imagen)
			existing_Imagen.Imagen.delete(False)

class ReporteOfertaDestacado(models.Model):
	Producto = models.OneToOneField(Producto)
	Fecha = models.DateField(auto_now_add=True)
	class Meta:
		verbose_name_plural=u'Reporte Productos en Ofeta y Destacado'
	def __unicode__(self):
		return str(self.Producto.Descripcion) + " - " + str(self.Fecha)

class Estado(models.Model):
	Estado = models.CharField(max_length=45, help_text='Describe el estado del carrito', verbose_name=u'Estado de Carrito')
	class Meta:
		verbose_name_plural=u'Estados para el carrito'
	def __unicode__(self):
		return self.Estado

class Carrito(models.Model):
	Usuario = models.ForeignKey(User, help_text='Seleccionar el usuario', verbose_name=u'Usuario')
	Estado = models.ForeignKey(Estado, help_text='Estado de la orden de productos')
	class Meta:
		verbose_name_plural=u'Carrito'
	def __unicode__(self):
		return self.Usuario.username

class Detalle_Carrito(models.Model):
	Producto = models.ForeignKey(Producto, help_text='Código del producto seleccionado', verbose_name=u'Código de Producto')
	Cantidad = models.IntegerField(help_text='Cantidad de producto', verbose_name=u'Cantidad')
	Carrito = models.ForeignKey(Carrito, help_text='Carrito al que se va asignar', verbose_name=u'Carrito', null=True, blank=True)
	class Meta:
		verbose_name_plural=u'Detalle de Carrito'
	def __unicode__(self):
		return self.Producto.Descripcion+" "+str(self.Cantidad)

class Pais(models.Model):
	Pais = models.CharField(max_length=45, help_text='Ingrese el nombre del país', verbose_name=u'País')
	class Meta:
		verbose_name=u'País'
		verbose_name_plural=u'Pais'
	def __unicode__(self):
		return self.Pais

class Region(models.Model):
	Region=models.CharField(max_length=100, verbose_name=u'Región')
	Pais=models.ForeignKey(Pais, verbose_name=u'País')
	class Meta:
		verbose_name_plural=u'Región'
	def __unicode__(self):
		return self.Region

class Ciudad(models.Model):
	Ciudad=models.CharField(max_length=200, verbose_name=u'Ciudad')
	Region=models.ForeignKey(Region, verbose_name=u'Región')
	Servicio_Domicilio=models.DecimalField(max_digits=5, decimal_places=2, verbose_name=u'Costo Flete')
	class Meta:
		verbose_name_plural=u'Ciudad'
	def __unicode__(self):
		return self.Ciudad

class Direccion_Orden(models.Model):
	Nombre = models.CharField(max_length=50, help_text='Ingrese el nombre completo del contacto', verbose_name=u'Nombre')
	Direccion = models.TextField(help_text='Ingrese la dirección para el envío', verbose_name=u'Dirección')
	Ciudad = models.ForeignKey(Ciudad, help_text='Ingresa una ciudad para la dirección')
	Region = models.ForeignKey(Region, help_text='Ingresar una región, estado o provincia', verbose_name=u'Estado')
	Pais = models.ForeignKey(Pais)
	Telefono = models.CharField(max_length=10, help_text='Ingrese el teléfono de contacto', verbose_name=u'Teléfono')
	Usuario = models.ForeignKey(User, help_text='Seleccionar el usuario', verbose_name=u'Usuario', blank=True, null=True)
	class Meta:
		verbose_name_plural=u'Dirección para orden de compra'
	def __unicode__(self):
		return self.Direccion +' '+ self.Ciudad.Ciudad +', '+ self.Region.Region +', '+ self.Pais.Pais

class Orden_Estado(models.Model):
	Estado=models.CharField(max_length=50, help_text='Estado de la orden', verbose_name=u'Estado')
	class Meta:
		verbose_name_plural=u'Estados para orden de compra'
	def __unicode__(self):
		return self.Estado

class Orden(models.Model):
	Fecha = models.DateField(help_text='Ingresar Fecha de la orden', verbose_name=u'Fecha', null=True, blank=True)
	Carrito = models.ForeignKey(Carrito, help_text='Ingrese el carrito que va a comprar', verbose_name=u'Carrito')
	Estado = models.ForeignKey(Orden_Estado, help_text='Estado de la orden de productos', null=True, blank=True)
	Direccion = models.ForeignKey(Direccion_Orden, help_text='Ingresar la dirección para el envío del producto', verbose_name=u'Dirección', null=True, blank=True)
	class Meta:
		verbose_name_plural=u'Orden de Compra'
	def __unicode__(self):
		return str(self.pk)

class Marca(models.Model):
	Marca = models.CharField(max_length=50, help_text='Nombre de la marca', verbose_name=u'Marca')
	Logotipo = models.ImageField(upload_to='img_marcas', verbose_name=u'Logotipo')
	Slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
	class Meta:
		verbose_name_plural=u'Marca de Producto'
	def __unicode__(self):
		return self.Marca

	def save(self, *args, **kwargs):
		self.Slug = defaultfilters.slugify(self.Marca)
		super(Marca, self).save(*args, **kwargs)

class Precio_Combustible(models.Model):
	Precio=models.DecimalField(max_digits=5, decimal_places=2, unique=True, help_text='Precio real en L. del combustible por galón ', verbose_name=u'Precio')
	Distancia_por_galon=models.DecimalField(max_digits=5, decimal_places=2, help_text='Distancia recorrida del vehiculo por galón', verbose_name=u'Consumo')
	Fecha=models.DateField(auto_now_add=True)
	def __unicode__(self):
		return 'L. '+ str(self.Precio)+' - Precio desde la fecha ' + str(self.Fecha)

class Servicio_Flete(models.Model):
	Lugar_Cliente=models.CharField(max_length=100, unique=True, help_text='Nombre del lugar destino del flete', verbose_name=u'Destino')
	Distancia=models.DecimalField(max_digits=5, decimal_places=2, help_text='Distancia del destino en kilometros', verbose_name=u'Distancia')
	Precio=models.ForeignKey(Precio_Combustible, help_text='Fecha del ultimo precio del combustible', verbose_name=u'Precio')
	class Meta:
		verbose_name_plural=u'Servicio de Flete'
	def __unicode__(self):
		return self.Lugar_Cliente

class DatosTransaccion(models.Model):
	Orden=models.ForeignKey(Orden)
	NumeroTransaccion=models.BigIntegerField()
	NumeroReferencia=models.BigIntegerField()
	NumeroAutorizacion=models.BigIntegerField()
	Fecha=models.DateTimeField(auto_now_add=True)
	class Meta:
		verbose_name_plural=u'Datos de Transacción'
	def __unicode__(self):
		return self.Orden.id

class Credito(models.Model):
	Fecha=models.DateField()
	Plazo=models.IntegerField()
	Monto=models.DecimalField(max_digits=6, decimal_places=2)
	Cuota=models.DecimalField(max_digits=6, decimal_places=2)
	Usuario=models.ForeignKey(User)
	class Meta:
		verbose_name_plural=u'Crédito'
	def __unicode__(self):
		return str(self.Fecha) + ' Monto L.' + str(self.Monto)

class Pagos(models.Model):
	Cuota=models.CharField(max_length=10)
	Fecha_Vencimiento=models.DateField()
	Valor_Cuota=models.DecimalField(max_digits=6, decimal_places=2)
	Mora=models.DecimalField(max_digits=5, decimal_places=2)
	Total_Pagado=models.DecimalField(max_digits=6, decimal_places=2)
	Estado=models.BooleanField(verbose_name=u'Pagado')
	Credito=models.ForeignKey(Credito)
	class Meta:
		verbose_name_plural=u'Pagos'
	def __unicode__(self):
		return str(self.Cuota)


class Contactos(models.Model):
	nombre = models.CharField(max_length=150)
	cargo = models.CharField(max_length=150, blank=True, null=True, help_text='Opcional')
	email = models.EmailField()
	email2 = models.EmailField(blank=True, null=True, help_text='Opcional')
	telefono = models.CharField(max_length=10)
	telefono2 = models.CharField(max_length=10, blank=True, null=True, help_text='Opcional')
	class Meta:
		verbose_name_plural=u'Contactos'
	def __unicode__(self):
		return self.nombre

class FAQ(models.Model):
	pregunta=models.CharField(max_length=200)
	respuesta=models.TextField()
	class Meta:
		verbose_name_plural=u'FAQ'
	def __unicode__(self):
		return self.pregunta

class Jumbotron(models.Model):
	nombre_banner = models.CharField(max_length=100, verbose_name=u'Nombre Imagen')
	imagen_pc = models.ImageField(upload_to='jumbotron/pc', verbose_name=u'Imagen PC', blank=True, null=True)
	imagen_info = models.ImageField(upload_to='jumbotron/info', verbose_name=u'Imagen Info', blank=True, null=True)
	#imagen_movil = models.ImageField(upload_to='jumbotron/movil', verbose_name=u'Imagen movil', blank=True, null=True)
	url = models.URLField(max_length=1000, verbose_name=u'URL', blank=True, null=True)
	class Meta:
		verbose_name=u'Jumbotron'
		verbose_name_plural=u'Jumbotron'
	def __unicode__(self):
		return self.nombre_banner
@receiver(pre_delete, sender=Jumbotron)
def Jumbotron_delete(sender, instance, **kwargs):
	instance.imagen_pc.delete(False)

@receiver(pre_save, sender=Jumbotron)
def delete_old_Jumbotron(sender, instance, *args, **kwargs):
	if instance.pk:
		existing_Imagen = Jumbotron.objects.get(pk=instance.pk)
		if instance.imagen_pc and existing_Imagen.imagen_pc != instance.imagen_pc:
			existing_Imagen.imagen_pc.delete(False)

class EncuestaVentas(models.Model):
	nombre = models.CharField(max_length=100, verbose_name=u'Nombre', blank=True, null=True)
	telefono = models.CharField(max_length=10, verbose_name=u'Teléfono', blank=True, null=True)
	email = models.EmailField(max_length=50, verbose_name=u'Correo Electrónico', blank=True, null=True)
	comentario = models.TextField(verbose_name=u'Comentario', blank=True, null=True)
	fecha = models.DateField(auto_now_add=True)
	p1 = models.IntegerField(verbose_name=u'Pregunta 1')
	p2 = models.IntegerField(verbose_name=u'Pregunta 2')
	p3 = models.IntegerField(verbose_name=u'Pregunta 3')
	p4 = models.IntegerField(verbose_name=u'Pregunta 4')
	p5 = models.IntegerField(verbose_name=u'Pregunta 5')
	p6 = models.IntegerField(verbose_name=u'Pregunta 6')
	p7 = models.IntegerField(verbose_name=u'Pregunta 7')
	p8 = models.IntegerField(verbose_name=u'Pregunta 8')
	p9 = models.IntegerField(verbose_name=u'Pregunta 9')
	p10 = models.IntegerField(verbose_name=u'Pregunta 10')
	p11 = models.IntegerField(verbose_name=u'Pregunta 11')
	p12 = models.IntegerField(verbose_name=u'Pregunta 12')
	class Meta:
		verbose_name_plural=u'Encuesta Ventas'
	def __unicode__(self):
		return str(self.fecha)

class EncuestaSoporte(models.Model):
	nombre = models.CharField(max_length=100, verbose_name=u'Nombre', blank=True, null=True)
	telefono = models.CharField(max_length=10, verbose_name=u'Teléfono', blank=True, null=True)
	email = models.EmailField(max_length=50, verbose_name=u'Correo Electrónico', blank=True, null=True)
	comentario = models.TextField(verbose_name=u'Comentario', blank=True, null=True)
	atendio = models.CharField(max_length=50, verbose_name=u'Atendio', blank=True, null=True)
	tiempoReparacion = models.CharField(max_length=15, verbose_name=u'Tiempo de Reparación', blank=True, null=True)
	fecha = models.DateField(auto_now_add=True)
	p1 = models.IntegerField(verbose_name=u'Pregunta 1')
	p2 = models.IntegerField(verbose_name=u'Pregunta 2')
	p2_1 = models.IntegerField(verbose_name=u'Pregunta 2.1')
	p3 = models.IntegerField(verbose_name=u'Pregunta 3')
	p4 = models.IntegerField(verbose_name=u'Pregunta 4')
	p5 = models.IntegerField(verbose_name=u'Pregunta 5')
	p5_1 = models.IntegerField(verbose_name=u'Pregunta 5.1', blank=True, null=True)
	p6 = models.IntegerField(verbose_name=u'Pregunta 6')
	p7 = models.IntegerField(verbose_name=u'Pregunta 7')
	p8 = models.IntegerField(verbose_name=u'Pregunta 8')
	p9 = models.IntegerField(verbose_name=u'Pregunta 9')
	p10 = models.IntegerField(verbose_name=u'Pregunta 10')
	p11 = models.IntegerField(verbose_name=u'Pregunta 11')
	p12 = models.IntegerField(verbose_name=u'Pregunta 12')
	class Meta:
		verbose_name_plural=u'Encuesta Soporte'
	def __unicode__(self):
		return str(self.fecha)

class AccesosDirectos(models.Model):
	Index = models.IntegerField(help_text='Posición en el orden de vista', unique=True)
	Nombre = models.CharField(max_length=50, verbose_name=u'Nombre del Acceso')
	Imagen = models.ImageField(upload_to='accesos', verbose_name=u'Imagen', help_text='Imagen del acceso directo', blank=True, null=True)
	Url = models.URLField(max_length=100, blank=True, null=True)
	class Meta:
		verbose_name_plural=u'Acceso Directo'
	def __unicode__(self):
		return str(self.Index) + " " + self.Nombre

class FactorDiasNovedades(models.Model):
	Dias = models.BigIntegerField(help_text='Rango de días para abarcar productos en novedades')
	class Meta:
		verbose_name_plural=u'Factor Días Novedades'
	def __unicode__(self):
		return str(self.Dias) + ("días").decode("utf-8")