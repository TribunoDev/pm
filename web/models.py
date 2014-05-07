#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Detalle_Perfil(models.Model):
	RNP=models.CharField(max_length=20, help_text='RNP del Usuario', verbose_name=u'RNP')
	Direccion = models.CharField(max_length=250, help_text='Direccion residencial del usuario', verbose_name=u'Direccion', null=True, blank=True)
	Telefono = models.CharField(max_length=10, null=True, blank=True, help_text='Teléfono del usuario', verbose_name=u'Telefono')
	Usuario = models.ForeignKey(User, unique=True, help_text='Usuario al que pertenece la dirección', verbose_name=u'Usuario')

	def __unicode__(self):
		return self.Usuario.username

class Categoria(models.Model):
	CodigoCategoria = models.CharField(max_length=25)
	Categoria = models.CharField(max_length=50, unique=True, help_text='Nombre de la categoría', verbose_name=u'Categoría')

	def __unicode__(self):
		return self.Categoria

class SubCategoria(models.Model):
	CodigoSubcategoria = models.CharField(max_length=25)
	Subcategoria = models.CharField(max_length=50, help_text='Nombre de la subcategoría', verbose_name=u'Sub-categoría')
	Categoria = models.ForeignKey(Categoria, help_text='Define la categoría para una subcategoría', verbose_name=u'Categoría')
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
	def __unicode__(self):
		return self.Descripcion

class Imagen(models.Model):
	Producto = models.ForeignKey(Producto)
	def __unicode__(self):
		return self.Producto.Descripcion

class Detalle_Imagen(models.Model):
	Producto = models.ForeignKey(Imagen)
	Imagen = models.ImageField(upload_to='img_detalle')

#class Detalle_Imagen(models.Model):
#	Imagen = models.ImageField(upload_to='img_detalle',verbose_name=u'Imágen')
#	Producto, help_text='Producto asociado a la imagen', verbose_name=u'Producto')
#	class Meta:
#		verbose_name=u'Detalle Imagen'
#		verbose_name_plural=u'Detalle Imagen'
#	def __unicode__(self):
#		return str(self.Imagen)

class Estado(models.Model):
	Estado = models.CharField(max_length=45, help_text='Describe el estado del carrito', verbose_name=u'Estado de Carrito')
	def __unicode__(self):
		return self.Estado

class Carrito(models.Model):
	Usuario = models.ForeignKey(User, help_text='Seleccionar el usuario', verbose_name=u'Usuario')
	Estado = models.ForeignKey(Estado, help_text='Estado de la orden de productos')
	def __unicode__(self):
		return self.Usuario.username

class Detalle_Carrito(models.Model):
	Producto = models.ForeignKey(Producto, help_text='Código del producto seleccionado', verbose_name=u'Código de Producto')
	Cantidad = models.IntegerField(help_text='Cantidad de producto', verbose_name=u'Cantidad')
	Carrito = models.ForeignKey(Carrito, help_text='Carrito al que se va asignar', verbose_name=u'Carrito', null=True, blank=True)
	def __unicode__(self):
		return self.Producto.Descripcion+" "+str(self.Cantidad)

class Pais(models.Model):
	Pais = models.CharField(max_length=45, help_text='Ingrese el nombre del país', verbose_name=u'País')
	class Meta:
		verbose_name=u'Pais'
		verbose_name_plural=u'Paises'
	def __unicode__(self):
		return self.Pais

class Region(models.Model):
	Region=models.CharField(max_length=100, verbose_name=u'Región')
	Precio=models.DecimalField(max_digits=5, decimal_places=2, verbose_name=u'Precio')
	Pais=models.ForeignKey(Pais, verbose_name=u'País')
	def __unicode__(self):
		return self.Region

class Ciudad(models.Model):
	Ciudad=models.CharField(max_length=200, verbose_name=u'Ciudad')
	Region=models.ForeignKey(Region, verbose_name=u'Región')
	Servicio_Domicilio=models.DecimalField(max_digits=5, decimal_places=2, verbose_name=u'Costo Flete')
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

	def __unicode__(self):
		return self.Direccion +' '+ self.Ciudad +', '+ self.Region +', '+ self.Pais.Pais

class Orden_Estado(models.Model):
	Estado=models.CharField(max_length=50, help_text='Estado de la orden', verbose_name=u'Estado')
	
	def __unicode__(self):
		return self.Estado

class Orden(models.Model):
	Fecha = models.DateField(help_text='Ingresar Fecha de la orden', verbose_name=u'Fecha', null=True, blank=True)
	Carrito = models.ForeignKey(Carrito, help_text='Ingrese el carrito que va a comprar', verbose_name=u'Carrito')
	Estado = models.ForeignKey(Orden_Estado, help_text='Estado de la orden de productos', null=True, blank=True)
	Direccion = models.ForeignKey(Direccion_Orden, help_text='Ingresar la dirección para el envío del producto', verbose_name=u'Dirección', null=True, blank=True)
	def __unicode__(self):
		return str(self.pk)

class Marca(models.Model):
	Marca = models.CharField(max_length=50, help_text='Nombre de la marca', verbose_name=u'Marca')
	Logotipo = models.ImageField(upload_to='img_marcas', verbose_name=u'Logotipo')

	def __unicode__(self):
		return self.Marca

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
	def __unicode__(self):
		return self.Lugar_Cliente

class DatosTransaccion(models.Model):
	Orden=models.ForeignKey(Orden)
	NumeroTransaccion=models.BigIntegerField()
	NumeroReferencia=models.BigIntegerField()
	NumeroAutorizacion=models.BigIntegerField()
	Fecha=models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.Orden.id

class Credito(models.Model):
	Fecha=models.DateField()
	Plazo=models.IntegerField()
	Monto=models.DecimalField(max_digits=6, decimal_places=2)
	Cuota=models.DecimalField(max_digits=6, decimal_places=2)
	Usuario=models.ForeignKey(User)
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
	def __unicode__(self):
		return str(self.Cuota)


class Contactos(models.Model):
	nombre = models.CharField(max_length=150)
	cargo = models.CharField(max_length=150, blank=True, null=True, help_text='Opcional')
	email = models.EmailField()
	email2 = models.EmailField(blank=True, null=True, help_text='Opcional')
	telefono = models.CharField(max_length=10)
	telefono2 = models.CharField(max_length=10, blank=True, null=True, help_text='Opcional')
	def __unicode__(self):
		return self.nombre

class FAQ(models.Model):
	pregunta=models.CharField(max_length=200)
	respuesta=models.TextField()
	def __unicode__(self):
		return self.pregunta
