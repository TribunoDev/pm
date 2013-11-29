# -*- coding:utf-8 -*-
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from web.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from web.forms import SignUpForm, Detalle_CarritoForm
from datetime import date

#Vista que retorna la pagina de inicio
def inicio(request):
	if not request.user.is_anonymous():
		usuario = request.user
		return render_to_response('index.html',{'usuario':usuario, 'centinela':True}, context_instance=RequestContext(request))
	else:
		return render_to_response('index.html', context_instance=RequestContext(request))

#Vista que retorna la ventana de inicio de sesion
def ingresar(request):
	if not request.user.is_anonymous():
	 	return HttpResponseRedirect('/home')

	if request.method=='POST':
		frmSesion = AuthenticationForm(request.POST)
		if frmSesion.is_valid():
			usuario = request.POST["username"]
			clave = request.POST["password"]
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/home')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request))
	else:
		frmSesion = AuthenticationForm()
	return render_to_response('inicio-sesion.html', context_instance=RequestContext(request))

@login_required()
def home(request):
	usuario = request.user
	return render_to_response('index.html',{'usuario':usuario, 'centinela':True}, context_instance=RequestContext(request))

#Vista que retorna la pagina de registro de usuario
def registrar(request):
	if request.method=='POST':
		frmUser = SignUpForm(request.POST)
		if frmUser.is_valid():
			#Procesar los datos con form.cleaned_data
			usuario = frmUser.cleaned_data["username"]
			contrasena = frmUser.cleaned_data["password"]
			email = frmUser.cleaned_data["email"]
			nombres = frmUser.cleaned_data["first_name"]
			apellidos = frmUser.cleaned_data["last_name"]
			#En este punto el usuario es un objeto de User y esta listo para ser
			#almacenado en la base de datos
			user = User.objects.create_user(usuario, email, contrasena)
			user.first_name = nombres
			user.last_name = apellidos

			#Guardar el nuevo usuario
			user.save()

			return HttpResponseRedirect(reverse('registrado'))
	else:
		frmUser = SignUpForm()

	return render_to_response('registro.html', context_instance=RequestContext(request))

def registrado(request):
 	return render_to_response('registrado.html', context_instance=RequestContext(request))

#Vista que devuelve las marcas de los productos
def marcas(request):
	marca = Marca.objects.all()
	if not request.user.is_anonymous():
		usuario = request.user
		return render_to_response('marcas.html',{'marcas': marca, 'usuario':usuario, 'centinela':True}, context_instance=RequestContext(request))
	else:
		return render_to_response('marcas.html', {'marcas': marca}, context_instance=RequestContext(request))

#Vista que retorna los productos por cada marca
def marca_producto(request, id_marca):
	marca = get_object_or_404(Marca, pk=id_marca)
	productos = Producto.objects.filter(Descripcion__icontains=marca)
	if request.user.is_authenticated():
		usuario = request.user
		return render_to_response('productos-marcas.html', {'marca':marca,'productos':productos,'usuario':usuario, 'centinela':True}, context_instance=RequestContext(request))
	else:
		return render_to_response('productos-marcas.html', {'marca':marca, 'productos':productos}, context_instance=RequestContext(request))

#Vista para devolver los productos con categoria "Novedades"
def destacados(request):
	destacados = Producto.objects.filter(Destacado__exact=True)
	return render_to_response('contenido-productos.html', {'datos': destacados}, context_instance= RequestContext(request))

#Vista que devuelve los productos que estan en la categoria de Ofertas
def ofertas(request):
	ofertas = Producto.objects.filter(Oferta__exact=True)
	return render_to_response('contenido-productos.html', {'datos':ofertas}, context_instance=RequestContext(request))

#Vista que genera los item de la pestaña productos en el menu principal
def catalogo_productos(request):
	categorias = Categoria.objects.all()
	subcategorias = SubCategoria.objects.all()
	total_sub = SubCategoria.objects.count()
	return render_to_response('categorias-productos.html', {'categorias':categorias, 'subcategorias':subcategorias}, context_instance=RequestContext(request))

#Vista que retorna los productos filtrando por subcategorias
def ver_subcategoria(request, id_subcat):
	subcat = get_object_or_404(SubCategoria, pk=id_subcat)
	productos = Producto.objects.filter(Subcategoria=subcat)
	if not request.user.is_anonymous():
		return render_to_response('productos-subcategoria.html', {'datos':subcat ,'productos': productos, 'usuario': request.user, 'centinela': True}, context_instance=RequestContext(request))
	else:
		return render_to_response('productos-subcategoria.html', {'datos':subcat ,'productos': productos}, context_instance=RequestContext(request))

#Vista que retorna el detalle de cada producto
def detalle_producto(request, id_producto):
	detalle = get_object_or_404(Producto, pk=id_producto)
	if not request.user.is_anonymous():
		return render_to_response('detalle-producto.html', {'detalle':detalle, 'usuario': request.user, 'centinela':True}, context_instance=RequestContext(request))
	else:
		return render_to_response('detalle-producto.html', {'detalle':detalle}, context_instance=RequestContext(request))

#Vista que devuelve los resultados de una busqueda
def buscar(request):
	if request.method=='POST':
		buscar = request.POST["txtBuscar"]
		resultado = Producto.objects.filter(Descripcion__icontains=buscar)
	if not request.user.is_anonymous():
		return render_to_response('resultado-busqueda.html',{'resultado':resultado,'dato': buscar, 'usuario':request.user,'centinela':True}, context_instance=RequestContext(request))
	else:
		return render_to_response('resultado-busqueda.html',{'resultado':resultado,'dato': buscar}, context_instance=RequestContext(request))

#Vista para generar una orden de compra
@login_required(login_url='/ingresar/')
def agregar_carrito(request):
	#Variables 
	usuario = request.user
	idEstado = Estado.objects.get(id=1)
	if request.is_ajax():
		if request.method == 'POST':
			formulario = Detalle_CarritoForm(request.POST)
			if formulario.is_valid:
				qset = (
					Q(Usuario=usuario)&
					Q(Estado=1)
					)
				cantCar = Carrito.objects.filter(qset).count()
				if cantCar == 0:
					carrito = Carrito(
						Usuario = usuario,
						Estado = idEstado
						)
					carrito.save()
			
				codProd = request.POST['Producto']
				cantidad = request.POST['Cantidad']

				carrito = Carrito.objects.get(Estado=1, Usuario=usuario)
				producto = Producto.objects.get(Codigo=codProd)

				if Detalle_Carrito.objects.filter(Producto=codProd, Carrito=carrito).count() == 1:
					detalle = Detalle_Carrito.objects.get(Producto = codProd, Carrito=carrito)
					cantidadTotal = detalle.Cantidad + int(cantidad)
					detalle.Cantidad = cantidadTotal
					detalle.save()
				else:
					detalleCar = Detalle_Carrito(
						Producto = producto,
						Cantidad = int(cantidad),
						Carrito = carrito
						)
					detalleCar.save()		
	return render_to_response('mensaje-carrito.html', {'cantidad':cantidad}, context_instance=RequestContext(request))

#Vista que retorna el total en el carrito
def datos_carrito(request):
	cantidad = 0
	precio = 0
	if not request.user.is_anonymous():
		usuario = request.user

	if request.is_ajax():
		estado = Estado.objects.get(id=1)
		carrito = Carrito.objects.get(Usuario=usuario, Estado=estado)
		detalle = Detalle_Carrito.objects.filter(Carrito = carrito)
		for item in detalle:
			cantidad += item.Cantidad
			precio += item.Producto.Precio * item.Cantidad

		return render_to_response('datos-carrito.html', {'cantidad': cantidad, 'subtotal':precio}, context_instance=RequestContext(request))

def item_carrito(request):
	cantidad = 0
	if not request.user.is_anonymous():
		usuario = request.user

	if request.is_ajax():
		estado = Estado.objects.get(id=1)
		carrito = Carrito.objects.get(Usuario=usuario, Estado=estado)
		detalle = Detalle_Carrito.objects.filter(Carrito = carrito)
		for item in detalle:
			cantidad += item.Cantidad		
	return HttpResponse(simplejson.dumps({'cantidad':cantidad}), mimetype='application/json')

@login_required(login_url='/ingresar/')
def carrito(request):
	if not request.user.is_anonymous():
		usuario = request.user

	carrito = Carrito.objects.get(Usuario=usuario, Estado=1)
	detalle = Detalle_Carrito.objects.filter(Carrito=carrito)

	return render_to_response('carrito.html',{'usuario':usuario, 'centinela':True, 'detalle':detalle}, context_instance=RequestContext(request))

def form_editar_cantidad(request):
	if request.is_ajax():
		if request.method == 'POST':
			idDetalle = request.POST['idDetalle']
			detalle = Detalle_Carrito.objects.get(id=idDetalle)
	return render_to_response('form-editar-cantidad.html', {'detalle':detalle}, context_instance=RequestContext(request))

def actualizar_cantidad(request):
	if not request.user.is_anonymous():
		usuario = request.user
	if request.is_ajax():
		if request.method == 'POST':
			cantidad = request.POST['Cantidad']
			producto = request.POST['Producto']

			carrito = Carrito.objects.get(Usuario=usuario, Estado=1)
			producto = Producto.objects.get(Codigo=producto)
			detalle = Detalle_Carrito.objects.get(Producto=producto, Carrito=carrito)
			detalle.Cantidad = cantidad
			detalle.save()

	return render_to_response('item-cantidad.html',{'item':detalle}, context_instance=RequestContext(request))

def eliminar_item_detalle(request):
	if request.is_ajax():
		if request.method == 'POST':
			idDetalle = request.POST['idDetalle']
			detalle = Detalle_Carrito.objects.filter(id=idDetalle).delete()
	return HttpResponse(simplejson.dumps({'dato':detalle}), mimetype='application/json')