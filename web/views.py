# -*- coding:utf-8 -*-
from django.db.models import Q, Sum, Count
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from web.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from web.forms import *
from datetime import date
from django.core.mail import EmailMessage
import suds
from suds.client import Client
from datetime import datetime, timedelta, date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

centinela = False

def intcomma(n):
	sign = '-' if n < 0 else ''
	n = str(abs(n)).split('.')
	dec = '.00' if len(n) == 1 else '.' + n[1]
  	n = n[0]
  	m = len(n)
  
  	return sign + (','.join([n[0:m%3]] + [n[i:i+3] for i in range(m%3, m, 3)])).lstrip(',') + dec

def images_destacados():
	listaDestacados = []
	pDestacados = Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')
	contar = 0
	for pD in pDestacados:
		if contar == 2:
			break
		else:
			cImgD = Detalle_Imagen.objects.filter(Producto=pD).count()
			if cImgD > 0:
				contar = contar + 1
				destacados = {
					'Codigo':pD.pk,
					'Descripcion':pD.Descripcion,
					'Precio': intcomma(pD.Precio)
				}
				listaDestacados.append(destacados)
				
	return listaDestacados

def images_ofertas():
	listaOfertas=[]
	pOfertas = Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')
	contar = 0
	for pO in pOfertas:
		if contar == 2:
			break
		else:
			cImgO = Detalle_Imagen.objects.filter(Producto=pO).count()
			if cImgO > 0:
				contar = contar + 1
				ofertas = {
					'Codigo':pO.pk,
					'Descripcion':pO.Descripcion,
					'Precio': intcomma(pO.Precio)
				}
				listaOfertas.append(ofertas)
	return listaOfertas

def images_novedades():
	listaNovedades=[]
	pNovedades = Producto.objects.filter(Fecha__month=datetime.now().month).order_by('?')
	contar = 0
	for pN in pNovedades:
		if contar == 2:
			break
		else:
			cImgN = Detalle_Imagen.objects.filter(Producto=pN).count()
			if cImgN > 0:
				contar = contar + 1
				novedades = {
					'Codigo':pN.pk,
					'Descripcion':pN.Descripcion,
					'Precio': intcomma(pN.Precio)
				}
				listaNovedades.append(novedades)
	return listaNovedades

#Vista que retorna la pagina de inicio
def inicio(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	return render_to_response('index.html',diccionario, context_instance=RequestContext(request))

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

@login_required(login_url='/ingresar/')
def home(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['usuario']=request.user
	diccionario['centinela']=True
	return render_to_response('index.html',diccionario, context_instance=RequestContext(request))

#Vista que retorna la pagina de registro de usuario
def registrar(request):
	if request.method=='POST':
		telefono = request.POST['Telefono']
		direccion = request.POST['Direccion']
		rnp=request.POST['RNP']
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

			#Guardar la direccion del nuevo usuario
			usuario = User.objects.get(username=usuario)
			detalle_perfil = Detalle_Perfil(
				RNP=rnp,
				Telefono = telefono,
				Direccion = direccion,
				Usuario = usuario
				)
			detalle_perfil.save()

			#Crear un carrito por default para el usuario
			c = Carrito(
				Usuario = usuario,
				Estado = Estado.objects.get(id=1)
				)
			c.save()

			acceso = authenticate(username=usuario, password=contrasena)
			login(request, acceso)
			return HttpResponseRedirect('/home')
	else:
		frmUser = SignUpForm()

	return render_to_response('registro.html', context_instance=RequestContext(request))

def registrado(request):
 	return render_to_response('registrado.html', context_instance=RequestContext(request))

#Vista que devuelve las marcas de los productos
def marcas(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= images_destacados()
	diccionario['ofertas']= images_ofertas()
	diccionario['novedades'] = images_novedades()
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
		
	return render_to_response('marcas.html', diccionario, context_instance=RequestContext(request))

#Vista que retorna los productos por cada marca
def marca_producto(request, id_marca):
	diccionario={}
	listaSubCat=[]
	pMarcas=[]
	marca=get_object_or_404(Marca, pk=id_marca)
	diccionario['marcas']=Marca.objects.all()
	diccionario['totalProductos'] = Producto.objects.filter(Descripcion__icontains=" "+marca.Marca+" ").count()
	productos = Producto.objects.filter(Descripcion__icontains=" "+marca.Marca+" ")
	allImages = Detalle_Imagen.objects.all().order_by('Imagen')
	for producto in productos:
		if Detalle_Imagen.objects.filter(Producto=producto).count() > 0:
			allImages = Detalle_Imagen.objects.filter(Producto=producto)[:1]
			archImg = allImages[0]
			archImg = archImg.Imagen
		else:
			archImg = "img_detalle/sin_imagen.png"
		infoProducto = {
			'Codigo': producto.Codigo,
			'Descripcion': producto.Descripcion,
			'Precio': intcomma(producto.Precio),
			'Oferta': producto.Oferta,
			'Imagen': archImg
		}
		pMarcas.append(infoProducto)

	subCat = SubCategoria.objects.all()
	for sC in subCat:
		contarProdSub = Producto.objects.filter(Descripcion__icontains=" "+marca.Marca+"", Subcategoria=sC.pk).count()
		if contarProdSub > 0:
			subcategorias = {
				'CodigoSubcategoria': sC.CodigoSubcategoria,
				'Subcategoria': sC.Subcategoria,
				'Categoria': sC.Categoria
			}
			listaSubCat.append(subcategorias)

	diccionario['subcategorias'] = listaSubCat
	diccionario['marca']=marca
	paginador = Paginator(pMarcas, 18)
	pagina = request.GET.get('page','1')
	
	try:
		pagina = int(request.GET.get('page','1'))
		productos = paginador.page(pagina)
	except PageNotAnInteger:
		pagina = 1
	except EmptyPage:
		productos = paginador.page(paginador.num_pages)

	startPage = max(pagina - 2, 1)
	if startPage <= 3:
		startPage = 1

	endPage = pagina + 2 + 1
	if endPage >= paginador.num_pages - 1:
		endPage = paginador.num_pages + 1

	page_number = []

	for n in range(startPage, endPage):
		if n > 0 and n <= paginador.num_pages:
			page_number.append(n)

	diccionario['page_number']=page_number

	diccionario['productos'] = productos
	diccionario['destacados']= images_destacados()
	diccionario['ofertas']= images_ofertas()
	diccionario['novedades'] = images_novedades()
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	return render_to_response('productos-marcas.html', diccionario, context_instance=RequestContext(request))

def filtro_marca_subcategoria(request):
	diccionario={}
	pSM=[]
	if request.is_ajax() and request.method == 'POST':

		if request.POST['subcategoria'] == 'all':
			diccionario['totalProductos'] = Producto.objects.filter(Descripcion__icontains=" "+request.POST['marca']+" ").count()

			productos = Producto.objects.filter(Descripcion__icontains=" "+request.POST['marca']+" ")

		else:
			diccionario['totalProductos'] = Producto.objects.filter(Descripcion__icontains=" "+request.POST['marca']+" ", Subcategoria=SubCategoria.objects.get(Subcategoria=request.POST['subcategoria'])).count()
			productos = Producto.objects.filter(Descripcion__icontains=" "+request.POST['marca']+" ", Subcategoria=SubCategoria.objects.get(Subcategoria=request.POST['subcategoria']))

		for producto in productos:
			if Detalle_Imagen.objects.filter(Producto=producto).count() > 0:
				allImages = Detalle_Imagen.objects.filter(Producto=producto)[:1]
				archImg = allImages[0]
				archImg = archImg.Imagen
			else:
				archImg = "img_detalle/sin_imagen.png"
			infoProducto = {
				'Codigo': producto.Codigo,
				'Descripcion': producto.Descripcion,
				'Precio': intcomma(producto.Precio),
				'Oferta': producto.Oferta,
				'Imagen': archImg
			}
			pSM.append(infoProducto)

		paginador = Paginator(pSM, 18)
		try:
			pagina = int(request.GET.get('page','1'))
			productos = paginador.page(pagina)
		except PageNotAnInteger:
			productos = 1
		except EmptyPage:
			productos = paginador.page(paginador.num_pages)

		startPage = max(pagina - 2, 1)
		if startPage <= 3:
			startPage = 1

		endPage = pagina + 2 + 1
		if endPage >= paginador.num_pages - 1:
			endPage = paginador.num_pages + 1

		page_number = []

		for n in range(startPage, endPage):
			if n > 0 and n <= paginador.num_pages:
				page_number.append(n)

		diccionario['page_number']=page_number

		diccionario['productos']=productos
		return render_to_response('filtro-marca-subcategoria.html', diccionario, context_instance=RequestContext(request))
	else:
		raise Http404

#Vista para devolver los productos con categoria "Novedades"
def destacados(request):
	diccionario={}
	destacados=[]
	allImages = Detalle_Imagen.objects.all().order_by('Imagen')
	productos = Producto.objects.filter(Destacado__exact=True)[:12]
	for producto in productos:
		if Detalle_Imagen.objects.filter(Producto=producto).count() > 0:
			allImages = Detalle_Imagen.objects.filter(Producto=producto)[:1]
			archImg = allImages[0]
			archImg = archImg.Imagen
		else:
			archImg = "img_detalle/sin_imagen.png"
		infoProducto = {
			'Codigo': producto.Codigo,
			'Descripcion': producto.Descripcion,
			'Precio': intcomma(producto.Precio),
			'Oferta': producto.Oferta,
			'Imagen': archImg
		}
		destacados.append(infoProducto)

	diccionario['datos']=destacados
	return render_to_response('contenido-productos.html', diccionario, context_instance= RequestContext(request))

#Vista que devuelve los productos que estan en la categoria de Ofertas
def ofertas(request):
	diccionario={}
	ofertas=[]
	allImages = Detalle_Imagen.objects.all().order_by('Imagen')
	productos = Producto.objects.filter(Oferta__exact=True)[:12]
	for producto in productos:
		if Detalle_Imagen.objects.filter(Producto=producto).count() > 0:
			allImages = Detalle_Imagen.objects.filter(Producto=producto)[:1]
			archImg = allImages[0]
			archImg = archImg.Imagen
		else:
			archImg = "img_detalle/sin_imagen.png"
		infoProducto = {
			'Codigo': producto.Codigo,
			'Descripcion': producto.Descripcion,
			'Precio': intcomma(producto.Precio),
			'Oferta': producto.Oferta,
			'Imagen': archImg
		}
		ofertas.append(infoProducto)

	diccionario['datos']=ofertas
	return render_to_response('contenido-productos.html', diccionario, context_instance=RequestContext(request))

def novedades(request):
	diccionario={}
	novedades=[]
	mes=datetime.now().month
	productos = Producto.objects.filter(Fecha__month=mes)[:12]
	for producto in productos:
		if Detalle_Imagen.objects.filter(Producto=producto).count() > 0:
			allImages = Detalle_Imagen.objects.filter(Producto=producto)[:1]
			archImg = allImages[0]
			archImg = archImg.Imagen
		else:
			archImg = "img_detalle/sin_imagen.png"
		infoProducto = {
			'Codigo': producto.Codigo,
			'Descripcion': producto.Descripcion,
			'Precio': intcomma(producto.Precio),
			'Oferta': producto.Oferta,
			'Imagen': archImg
		}
		novedades.append(infoProducto)

	diccionario['datos']=novedades
	return render_to_response('contenido-productos.html', diccionario, context_instance=RequestContext(request))


#Vista que genera los item de la pestaña productos en el menu principal
def catalogo_productos(request):
	diccionario={}
	diccionario['categorias']=Categoria.objects.all()
	diccionario['subcategorias']=SubCategoria.objects.all()
	producto = Producto.objects.all()
	diccionario['total']=SubCategoria.objects.annotate(existencia=Count('producto'))
	return render_to_response('categorias-productos.html', diccionario, context_instance=RequestContext(request))



#Vista que retorna los productos filtrando por subcategorias
def ver_subcategoria(request, id_subcat):
	diccionario={}
	listaProducto = []
	listaOfertas = []
	listaDestacados = []
	listaNovedades = []
	subcat = get_object_or_404(SubCategoria, pk=id_subcat)
	diccionario['datos']=subcat
	diccionario['totalProductos']=Producto.objects.filter(Subcategoria=subcat).count()
	productos = Producto.objects.filter(Subcategoria=subcat)
	for producto in productos:
		if Detalle_Imagen.objects.filter(Producto=producto.Codigo).count() > 0:
			allImages = Detalle_Imagen.objects.filter(Producto=producto)[:1]
			archImg = allImages[0]
			archImg = archImg.Imagen
		else:
			archImg = "img_detalle/sin_imagen.png"
		infoProducto = {
			'Codigo': producto.Codigo,
			'Descripcion': producto.Descripcion,
			'Precio': intcomma(producto.Precio),
			'Oferta':producto.Oferta,
			'Imagen': archImg
		}
		listaProducto.append(infoProducto)

	paginador = Paginator(listaProducto, 18)
	
	try:
		pagina = int(request.GET.get('page','1'))
		productos = paginador.page(pagina)
	except PageNotAnInteger:
		pagina = 1
	except EmptyPage:
		productos = paginador.page(paginador.num_pages)

	startPage = max(pagina - 2, 1)
	if startPage <= 3:
		startPage = 1

	endPage = pagina + 2 + 1
	if endPage >= paginador.num_pages - 1:
		endPage = paginador.num_pages + 1

	page_number = []

	for n in range(startPage, endPage):
		if n > 0 and n <= paginador.num_pages:
			page_number.append(n)

	diccionario['page_number']=page_number

	listaMarcas = []
	if Marca.objects.all().count() > 0:
		for marca in Marca.objects.all():
			cP = Producto.objects.filter(Subcategoria=subcat, Descripcion__icontains=" "+marca.Marca+" ").count()
			if cP > 0:
				listaMarcas.append(marca)

	diccionario['listaMarcas']=listaMarcas
	diccionario['productos'] = productos
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= images_destacados()
	diccionario['ofertas'] = images_ofertas()
	diccionario['novedades'] = images_novedades()
	diccionario['detalle_img'] = Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	return render_to_response('productos-subcategoria.html', diccionario, context_instance=RequestContext(request))

def filtro_subcategoria_marca(request):
	diccionario={}
	pMS=[]
	if request.is_ajax() and request.method == 'POST':
		if request.POST['marca'] == 'all':
			diccionario['totalProductos']= Producto.objects.filter(Subcategoria=SubCategoria.objects.get(Subcategoria=request.POST['subcategoria'])).count()
			productos = Producto.objects.filter(Subcategoria=SubCategoria.objects.get(Subcategoria=request.POST['subcategoria']))
		else:
			marca = Marca.objects.get(id=request.POST['marca'])
			marca = " "+marca.Marca+" "
			diccionario['totalProductos'] = Producto.objects.filter(Descripcion__icontains=marca, Subcategoria=SubCategoria.objects.get(Subcategoria=request.POST['subcategoria'])).count()
			productos = Producto.objects.filter(Descripcion__icontains=marca, Subcategoria=SubCategoria.objects.get(Subcategoria=request.POST['subcategoria']))
		for producto in productos:
			if Detalle_Imagen.objects.filter(Producto=producto).count() > 0:
				allImages = Detalle_Imagen.objects.filter(Producto=producto)[:1]
				archImg = allImages[0]
				archImg = archImg.Imagen
			else:
				archImg = "img_detalle/sin_imagen.png"
			infoProducto = {
				'Codigo': producto.Codigo,
				'Descripcion': producto.Descripcion,
				'Precio': intcomma(producto.Precio),
				'Oferta': producto.Oferta,
				'Imagen': archImg
				}
			pMS.append(infoProducto)

		paginador = Paginator(pMS, 18)
		try:
			pagina = int(request.GET.get('page','1'))
			productos = paginador.page(pagina)
		except PageNotAnInteger:
			pagina = 1
		except EmptyPage:
			productos = paginador.page(paginador.num_pages)

		startPage = max(pagina - 2, 1)
		if startPage <= 3:
			startPage = 1

		endPage = pagina + 2 + 1
		if endPage >= paginador.num_pages - 1:
			endPage = paginador.num_pages + 1

		page_number = []

		for n in range(startPage, endPage):
			if n > 0 and n <= paginador.num_pages:
				page_number.append(n)

		diccionario['page_number']=page_number

		diccionario['productos']=productos
		return render_to_response('filtro-subcategoria-marca.html', diccionario, context_instance=RequestContext(request))
	else:
		raise Http404


#Vista que retorna el detalle de cada producto
def detalle_producto(request, id_producto):
	diccionario={}
	codProd = request.GET.get('id_producto')
	detalle = get_object_or_404(Producto, Codigo=id_producto)
	diccionario['cantidad'] = Detalle_Imagen.objects.filter(Producto=detalle).count()
	diccionario['imagenes'] = Detalle_Imagen.objects.filter(Producto=detalle).order_by('Imagen')
	diccionario['detalle']=detalle
	diccionario['precio']=intcomma(detalle.Precio)
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']=images_destacados()
	diccionario['ofertas']=images_ofertas()
	diccionario['novedades'] = images_novedades()
	diccionario['detalle_img']= Detalle_Imagen.objects.all().order_by('Imagen')
	diccionario['formulario']=ContactoForm()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	return render_to_response('detalle-producto.html', diccionario, context_instance=RequestContext(request))

#Vista que devuelve los resultados de una busqueda
def buscar(request):
	diccionario={}
	listaProducto = []
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= images_destacados()
	diccionario['ofertas']= images_ofertas()
	diccionario['novedades'] = images_novedades()
	diccionario['detalle_img']= Detalle_Imagen.objects.all()

	buscar = request.GET.get("txtBuscar")
	pagina = request.GET.get("pagina")
	diccionario['totalProductos'] = Producto.objects.filter(Descripcion__icontains=buscar).count()
	resultado = Producto.objects.filter(Descripcion__icontains=buscar)
	for producto in resultado:
		if Detalle_Imagen.objects.filter(Producto=producto).count() > 0:
			allImages=Detalle_Imagen.objects.filter(Producto=producto)[:1]
			archImg=allImages[0]
			archImg=archImg.Imagen
		else:
			archImg = "img_detalle/sin_imagen.png"
		infoProducto = {
			'Codigo': producto.Codigo,
			'Descripcion': producto.Descripcion,
			'Precio': intcomma(producto.Precio),
			'Destacado': producto.Destacado,
			'Oferta':producto.Oferta,
			'Imagen': archImg
		}
		listaProducto.append(infoProducto)

	diccionario['dato']=buscar
	paginador = Paginator(listaProducto, 18)
	try:
		pagina = int(request.GET.get('pagina','1'))
		resultado = paginador.page(pagina)
	except PageNotAnInteger:
		pagina = 1
	except EmptyPage:
		resultado = paginador.page(paginador.num_pages)

	startPage = max(pagina - 2, 1)
	if startPage <= 3:
		startPage = 1

	endPage = pagina + 2 + 1
	if endPage >= paginador.num_pages - 1:
		endPage = paginador.num_pages + 1

	page_number = []

	for n in range(startPage, endPage):
		if n > 0 and n <= paginador.num_pages:
			page_number.append(n)

	diccionario['page_number']=page_number
	diccionario['resultado'] = resultado

	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	return render_to_response('resultado-busqueda.html',diccionario, context_instance=RequestContext(request))

#Vista para generar una orden de compra
def agregar_carrito(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	if request.user.is_anonymous():
	 	return HttpResponseRedirect('/ingresar/')
	#Variables 
	cantidad = 0
	codProd = 0
	usuario = request.user
	idEstado = Estado.objects.get(id=1)
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
		diccionario['cantidad']=cantidad
		diccionario['usuario']=usuario
		diccionario['centinela']=True
		diccionario['marcas']=Marca.objects.all()
		diccionario['destacados']= images_destacados()
		diccionario['ofertas']= images_ofertas()
		diccionario['detalle_img']= Detalle_Imagen.objects.all()

	return HttpResponseRedirect('/carrito/')

#Vista que retorna el total en el carrito
def datos_carrito(request):
	diccionario={}
	cantidad = 0
	precio = 0
	estado = 0
	carrito = 0
	usuario = 0
	productoImagen =[]
	
	if request.is_ajax():
			estado = Estado.objects.get(id=1)
			if not request.user.is_anonymous():
				usuario = request.user
				carrito = Carrito.objects.get(Usuario=usuario, Estado=estado)
				detalle = Detalle_Carrito.objects.filter(Carrito = carrito)
				for item in detalle:
					cantidad += item.Cantidad
					precio += item.Producto.Precio * item.Cantidad
	diccionario['cantidad']=cantidad
	diccionario['subtotal']=intcomma(precio)
	diccionario['carrito']=carrito

	return render_to_response('datos-carrito.html',diccionario, context_instance=RequestContext(request))

#Vista que retorna la cantidad de productos y mostrarlo en la pestaña "Carrito" del menu
def item_carrito(request):
	cantidad = 0
	estado = 0
	if not request.user.is_anonymous():
		usuario = request.user
	
	#if Carrito.objects.filter(Usuario=usuario, Estado=estado).count() != 0:
		estado = Estado.objects.get(id=1)
		carrito = Carrito.objects.get(Usuario=usuario, Estado=estado)
		detalle = Detalle_Carrito.objects.filter(Carrito = carrito)
		for item in detalle:
			cantidad += item.Cantidad		
	return HttpResponse(json.dumps({'cantidad':cantidad}), content_type='application/json')

#Vista que retorna a la pagina de "Carrito"
@login_required(login_url='/ingresar/')
def carrito(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= images_destacados()
	diccionario['ofertas']= images_ofertas()
	diccionario['novedades'] = images_novedades()
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	return render_to_response('carrito.html',diccionario, context_instance=RequestContext(request))

#Vista que retorna formulario para editar cantidad de cada producto en carrito
def form_editar_cantidad(request):
	if request.is_ajax():
		if request.method == 'POST':
			idDetalle = request.POST['idDetalle']
			detalle = Detalle_Carrito.objects.get(id=idDetalle)
	return render_to_response('form-editar-cantidad.html', {'detalle':detalle}, context_instance=RequestContext(request))

#Vista que actualiza la cantidad de productos en cada item del carrito
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

#Vista que elimina un item del carrito
def eliminar_item_detalle(request):
	if request.is_ajax():
		if request.method == 'POST':
			idDetalle = request.POST['idDetalle']
			detalle = Detalle_Carrito.objects.filter(id=idDetalle).delete()
	return HttpResponse(json.dumps({'dato':detalle}), content_type='application/json')

#Vista que retorna a la pagina del perfil de usuario
@login_required(login_url='/ingresar/')
def perfil_usuario(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
		diccionario['uPerfil']=User.objects.get(id=request.user.id)
		if Detalle_Perfil.objects.filter(Usuario=request.user).count() > 0:
			diccionario['dPerfil']=Detalle_Perfil.objects.get(Usuario=request.user)
		diccionario['marcas']=Marca.objects.all()
		diccionario['destacados']= images_destacados()
		diccionario['novedades'] = images_novedades()
		diccionario['ofertas']= images_ofertas()
		diccionario['detalle_img']= Detalle_Imagen.objects.all()
	return render_to_response('perfil-usuario.html',diccionario, context_instance=RequestContext(request))

#Vista que devuelve informacion sobre el usuario
def info_usuario(request):
	usuario = False
	perfil = False
	if not request.user.is_anonymous():
		usuario = request.user
		usuario = User.objects.get(id=usuario.id)
		if Detalle_Perfil.objects.filter(Usuario=usuario).count() > 0:
			perfil = Detalle_Perfil.objects.get(Usuario=usuario)
	return render_to_response('info-usuario.html',{'usuario':usuario, 'perfil':perfil}, context_instance=RequestContext(request))

#Vista que retorna en ajax los datos de los productos que ya estan en el carrito 
def items_en_carrito(request):
	diccionario={}
	carrito = 0
	detalleCarrito = []
	if not request.user.is_anonymous():
		usuario = request.user
		carrito = Carrito.objects.get(Usuario=usuario, Estado=1)
	if Detalle_Carrito.objects.filter(Carrito=carrito).count() > 0:
		for item in Detalle_Carrito.objects.filter(Carrito=carrito):
			producto = Producto.objects.get(Codigo=item.Producto.Codigo)
			if Detalle_Imagen.objects.filter(Producto=producto.Codigo).count() > 0:
				allImages = Detalle_Imagen.objects.filter(Producto=producto.Codigo)[:1]
				archImg = allImages[0]
				archImg = archImg.Imagen
			else:
				archImg = "img_detalle/sin_imagen.png"
			detalle = {
				'id': item.pk,
				'Carrito': carrito,
				'Imagen': archImg,
				'Producto': Producto.objects.get(Codigo=item.Producto.Codigo),
				'Cantidad': item.Cantidad,
				'Precio': intcomma(item.Producto.Precio)
				}
			detalleCarrito.append(detalle)
		diccionario['detalle']=detalleCarrito
		template = 'items-en-carrito.html'
	else:
		template = 'no-hay-items-carrito.html'
	return render_to_response(template,diccionario, context_instance=RequestContext(request))

#Vista que devuelve a la pagina ofertas
def productos_ofertas(request):
	diccionario={}
	ofertas = []
	centinela = False
	usuario = ""
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	diccionario['marcas']=Marca.objects.all()
	pOfertas = Producto.objects.filter(Oferta__exact=True)
	diccionario['totalProductos'] = Producto.objects.filter(Oferta__exact=True).count()
	for producto in Producto.objects.filter(Oferta__exact=True):
		if Detalle_Imagen.objects.filter(Producto=producto).count() > 0:
			allImages=Detalle_Imagen.objects.filter(Producto=producto)[:1]
			archImg=allImages[0]
			archImg=archImg.Imagen
		else:
			archImg = "img_detalle/sin_imagen.png"

		infoProducto = {
		'Codigo': producto.Codigo,
		'Descripcion': producto.Descripcion,
		'Precio': intcomma(producto.Precio),
		'Destacado': producto.Destacado,
		'Oferta':producto.Oferta,
		'Imagen': archImg
		}
		ofertas.append(infoProducto)

	paginador = Paginator(ofertas, 18)
	try:
		pagina = int(request.GET.get('page','1'))
		ofertas = paginador.page(pagina)
	except PageNotAnInteger:
		pagina = 1
	except EmptyPage:
		ofertas = paginador.page(paginador.num_pages)

	startPage = max(pagina - 2, 1)
	if startPage <= 3:
		startPage = 1

	endPage = pagina + 2 + 1
	if endPage >= paginador.num_pages - 1:
		endPage = paginador.num_pages + 1

	page_number = []

	for n in range(startPage, endPage):
		if n > 0 and n <= paginador.num_pages:
			page_number.append(n)

	diccionario['page_number']=page_number

	diccionario['destacados'] = images_destacados()
	diccionario['novedades'] = images_novedades()
	diccionario['detalle_img'] = Detalle_Imagen.objects.all()
	diccionario['productos'] = ofertas
	return render_to_response('ofertas.html', diccionario, context_instance=RequestContext(request))


def productos_destacados(request):
	diccionario={}
	destacados=[]
	centinela = False
	usuario = ""
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	diccionario['marcas']=Marca.objects.all()
	diccionario['totalProductos'] = Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).count()

	for producto in Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?'):
		if Detalle_Imagen.objects.filter(Producto=producto).count() > 0:
			allImages=Detalle_Imagen.objects.filter(Producto=producto)[:1]
			archImg=allImages[0]
			archImg=archImg.Imagen
		else:
			archImg = "img_detalle/sin_imagen.png"

		infoProducto = {
		'Codigo': producto.Codigo,
		'Descripcion': producto.Descripcion,
		'Precio': intcomma(producto.Precio),
		'Destacado': producto.Destacado,
		'Oferta':producto.Oferta,
		'Imagen': archImg
		}
		destacados.append(infoProducto)


	paginador = Paginator(destacados, 18)
	try:
		pagina = int(request.GET.get('page','1'))
		destacados = paginador.page(pagina)
	except PageNotAnInteger:
		pagina = 1
	except EmptyPage:
		destacados = paginador.page(paginador.num_pages)

	startPage = max(pagina - 2, 1)
	if startPage <= 3:
		startPage = 1

	endPage = pagina + 2 + 1
	if endPage >= paginador.num_pages - 1:
		endPage = paginador.num_pages + 1

	page_number = []

	for n in range(startPage, endPage):
		if n > 0 and n <= paginador.num_pages:
			page_number.append(n)

	diccionario['page_number']=page_number


	diccionario['ofertas'] = images_ofertas()
	diccionario['novedades'] = images_novedades()
	diccionario['detalle_img'] = Detalle_Imagen.objects.all()
	diccionario['productos'] = destacados
	return render_to_response('destacados.html', diccionario, context_instance=RequestContext(request))


#Vista que retorna los datos del servicio de flete
def servicio_flete(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')[:2]
	diccionario['ofertas']= Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')[:2]
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	diccionario['lugar']=Servicio_Flete.objects.all()
	return render_to_response('servicio-flete.html', diccionario, context_instance=RequestContext(request))

def enviar_email(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')[:2]
	diccionario['novedades'] = Producto.objects.filter(Fecha__month=datetime.now().month).order_by('?')[:2]
	diccionario['ofertas']= Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')[:2]
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	if request.method=='POST':
		formulario=ContactoForm(request.POST)
		if formulario.is_valid():
			titulo = 'Mensaje desde la pagina web de Paper & More'
			amigo=formulario.cleaned_data['amigo']
			contenido = 'Mensaje enviado por: ' + formulario.cleaned_data['correo'] + "\n\n"
			contenido+=formulario.cleaned_data['mensaje'] + "\n\n"
			contenido+='Da click en el siguiente enlace para ver la informacion compartida:\n'
			contenido+=formulario.cleaned_data['url']+ "\n"
			
			correo=EmailMessage(titulo, contenido, to=[amigo])
			correo.send()
		else:
			formulario = ContactoForm()
	return render_to_response('email-enviado.html',diccionario, context_instance=RequestContext(request))

def envio_datos_pago(request):
	if not request.user.is_anonymous():
		if request.method=='POST':
			carrito = Carrito.objects.get(Usuario=request.user, Estado=Estado.objects.get(pk=1))
			detalle = Detalle_Carrito.objects.filter(Carrito = carrito)
			precio=0
			for item in detalle:
				precio += item.Producto.Precio * item.Cantidad
			Tot=precio

			if Tot >= 15000:
				return HttpResponseRedirect('/enviar-direccion/')
			if Tot<15000:
				return HttpResponseRedirect('/enviar-pago-carrito/')

def envio_direccion(request):
	estado=Estado.objects.get(pk=1)
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= images_destacados()
	diccionario['ofertas']= images_ofertas()
	diccionario['novedades'] = images_novedades()
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
		diccionario['frmDireccion']=Direccion_OrdenForm()
		diccionario['direccion']=Direccion_Orden.objects.filter(Usuario=request.user)
		diccionario['carrito']=Carrito.objects.get(Usuario=request.user, Estado=estado)
		return render_to_response('enviar-direccion-orden.html', diccionario, context_instance=RequestContext(request))
	else:
		HttpResponseRedirect('/ingresar/')
		

def envio_pago(request):
	cantidad=0
	precio=0
	diccionario={}
	diccionario['frmDireccion']=Direccion_OrdenForm()
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= images_destacados()
	diccionario['ofertas']= images_ofertas()
	diccionario['novedades'] = images_novedades()
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
		estado = Estado.objects.get(id=1)
		carrito = Carrito.objects.get(Usuario=request.user, Estado=estado)
		detalle = Detalle_Carrito.objects.filter(Carrito = carrito)
		for item in detalle:
			cantidad += item.Cantidad
			precio += item.Producto.Precio * item.Cantidad
		diccionario['cantidad']=cantidad
		diccionario['subtotal']=intcomma(precio)
		diccionario['carrito']=carrito

		anos=[]
		anoActual = date.today()
		anoMax = anoActual + timedelta(7300)
		while anoActual <= anoMax:
			anos.append(anoActual)
			anoActual += timedelta(365)

		diccionario['anos']=anos

	if request.method == 'POST':
		idDir=request.POST['idDireccion']
		diccionario['direccion']=Direccion_Orden.objects.get(Usuario=request.user, pk=idDir)
		dire=Direccion_Orden.objects.get(pk=idDir)
		diccionario['total']=precio+dire.Ciudad.Servicio_Domicilio
		diccionario['region']=dire
				
	return render_to_response('enviar-pago.html', diccionario, context_instance=RequestContext(request))

def envio_pago_directo(request):
	cantidad=0
	precio=0
	diccionario={}
	diccionario['usuario']=request.user
	diccionario['centinela']=True
	carrito=Carrito.objects.get(Usuario=request.user, Estado=Estado.objects.get(pk=1))
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= images_destacados()
	diccionario['ofertas']= images_ofertas()
	diccionario['novedades'] = images_novedades()
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	detalle = Detalle_Carrito.objects.filter(Carrito = carrito)
	anos=[]
	anoActual = date.today()
	anoMax = anoActual + timedelta(7300)
	while anoActual <= anoMax:
		anos.append(anoActual)
		anoActual += timedelta(365)

	diccionario['anos']=anos
	for item in detalle:
		cantidad += item.Cantidad
		precio += item.Producto.Precio * item.Cantidad
	diccionario['cantidad']=cantidad
	diccionario['subtotal']=intcomma(precio)
	diccionario['carrito']=carrito
	return render_to_response('enviar-pago2.html', diccionario, context_instance=RequestContext(request))



def procesar_pago(request):
	diccionario={}
	if not request.user.is_anonymous():
		usuario = request.user
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	else:
		HttpResponseRedirect('/ingresar/')
	precio=0
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= images_destacados()
	diccionario['ofertas']= images_ofertas()
	diccionario['novedades'] = images_novedades()
	diccionario['detalle_img']= Detalle_Imagen.objects.all()

	if request.method=='POST':
		nT=request.POST['codTar']
		mT=request.POST['meses']
		aT=request.POST['anos']
		cvv=request.POST['CVV']
		fT=aT+mT
		tPago=request.POST['tipoPago']
		idDir=request.POST['idDireccion']
		carrito = Carrito.objects.get(Usuario=request.user, Estado=Estado.objects.get(pk=1))
		detalle = Detalle_Carrito.objects.filter(Carrito = carrito)
		for item in detalle:
			precio += item.Producto.Precio * item.Cantidad
		
		if len(idDir) > 0:
			dire=Direccion_Orden.objects.get(pk=idDir)
			Tot=precio+dire.Ciudad.Servicio_Domicilio
		else:
			Tot=precio

		url='https://dpp.credomatic.com:50581/WebServices/CSP/Authorizer2/Authorize.asmx?WSDL'
		cli = Client(url)

		aut = cli.factory.create('clsAuthenticationHeader')
		aut.UserName='hn_wusr_dev'
		aut.Password='WsrHn_2013'

		pet = cli.factory.create('clsWSRequestData')
		pet.transactionType = 'SALE'
		pet.terminalId = 'PRUPAM01'
		pet.entryMode = 'M'
		pet.accountNumber = nT
		pet.expirationDate = fT
		pet.totalAmount = Tot

		diccionario['carrito']=carrito

		try:
			template=0
			res = cli.service.executeTransaction(aut, pet)
			if res.responseCode=='00':
				car=Carrito.objects.get(Usuario=usuario, Estado=Estado.objects.get(pk=1))
				car.Estado=Estado.objects.get(pk=2)
				car.save()
				genOrd=Orden(
						Fecha=date.today(),
						Carrito=car,
						Estado=Orden_Estado.objects.get(pk=1),
					)
				genOrd.save()
				if len(idDir) > 0:
					genOrd=Orden.objects.get(Carrito=car)
					genOrd.Direccion=Direccion_Orden.objects.get(pk=idDir)
					genOrd.save()

				datosTrasn=DatosTransaccion(
						Orden=Orden.objects.get(Carrito=car),
						NumeroTransaccion=res.transactionId,
						NumeroReferencia=res.referenceNumber,
						NumeroAutorizacion=res.authorizationNumber,
					)
				datosTrasn.save()


				diccionario['resp']=res
				template='transaccion-exitosa.html'
				o = Orden.objects.get(Carrito=car)
				d=Detalle_Carrito.objects.filter(Carrito=car)
				u=User.objects.get(pk=request.user.id)
				titulo = 'Orden de Compra desde la tienda online.'
				desde='no_reply@pm.hn'
				amigo='mjbc007@gmail.com'
				html='<h2>Detalle de Orden</h2>'
				html+='<p>Numero de Orden: '+ str(o.id) +'</p>'
				html+='<p>Nombre del Cliente: '+ str(u.first_name) + ' ' + str(u.last_name)+ '</p>'
				if len(idDir) > 0:
					html+='<p>Direccion de envio: '+ str(o.Direccion.Direccion)+ ', '+ str(o.Direccion.Ciudad)+ ', '+ str(o.Direccion.Region)+ ', '+ str(o.Direccion.Pais) + '</p>'
				html+='<table style="text-align:center">'
				html+='<thead>'
				html+='<tr>'
				html+='<th>Codigo del Producto</th>'
				html+='<th>Descripcion</th>'
				html+='<th>Cantidad</th>'
				html+='<th>Precio</th>'
				html+='</tr>'
				html+='</thead>'
				html+='<tbody>'
				for item in d:
					html+='<tr>'
					html+='<td>'+ str(item.Producto.Codigo) +'</td>'
					html+='<td>'+ str(item.Producto.Descripcion) +'</td>'
					html+='<td>'+ str(item.Cantidad) +'</td>'
					html+='<td>'+ str(item.Producto.Precio) +'</td>'
					html+='</tr>'
				html+='</tbody>'
				html+='</table>'

				msg=EmailMessage(titulo,html, desde, [amigo])
				msg.content_subtype='html'
				msg.send()

			if res.responseCode=='05':
				template='transaccion-denegada.html'
			if res.responseCode=='NA':
				template='sin-sistema.html'
				diccionario['resp']=res
		except suds.WebFault, e:
			diccionario['error']=e
			
	return render_to_response(template, diccionario, context_instance=RequestContext(request))

def guardar_direccion(request):
	cantidad=0
	precio=0
	diccionario={}
	anos=[]
	anoActual = date.today()
	anoMax = anoActual + timedelta(7300)
	while anoActual <= anoMax:
		anos.append(anoActual)
		anoActual += timedelta(365)
	diccionario['anos']=anos
	if request.method == 'POST':
		frmDir = Direccion_OrdenForm(request.POST)
		if frmDir.is_valid():
			contacto = frmDir.cleaned_data['Nombre']
			idCiudad = frmDir.cleaned_data['Ciudad']
			idRegion = request.POST['Region']
			#region = Region.objects.get(id=idRegion)
			pais = frmDir.cleaned_data['Pais']
			direccion = frmDir.cleaned_data['Direccion']
			telefono = frmDir.cleaned_data['Telefono']
			Dir = Direccion_Orden(
					Nombre=contacto,
					Direccion=direccion,
					Ciudad=idCiudad,
					Region=Region.objects.get(pk=idRegion),
					Pais=pais,
					Telefono=telefono,
					Usuario=request.user
				)
			Dir.save()
			direccion=Direccion_Orden.objects.get(Nombre=contacto, Direccion=direccion, Ciudad=idCiudad, Region=idRegion, Pais=pais, Telefono=telefono, Usuario=request.user)
			diccionario['direccion']=direccion
			diccionario['usuario']=request.user
			diccionario['centinela']=True
			carrito=Carrito.objects.get(Usuario=request.user, Estado=Estado.objects.get(pk=1))
			diccionario['marcas']=Marca.objects.all()
			diccionario['destacados']= images_destacados()
			diccionario['ofertas']= images_ofertas()
			diccionario['novedades'] = images_novedades()
			diccionario['detalle_img']= Detalle_Imagen.objects.all()
			detalle = Detalle_Carrito.objects.filter(Carrito = carrito)
			#ciudad=Ciudad.objects.get(pk=idCiudad)
			for item in detalle:
				cantidad += item.Cantidad
				precio += item.Producto.Precio * item.Cantidad
			diccionario['cantidad']=cantidad
			diccionario['subtotal']=precio
			diccionario['total']=precio+direccion.Ciudad.Servicio_Domicilio
			diccionario['carrito']=carrito
			#diccionario['ciudad']=ciudad
			
			return render_to_response('enviar-pago.html', diccionario, context_instance=RequestContext(request))
			#return HttpResponse(json.dumps({'texto':texto}), content_type='application/json')
		else:
			return render_to_response('enviar-pago.html', diccionario, context_instance=RequestContext(request))

def editar_perfil(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
		diccionario['uPerfil']=User.objects.get(id=request.user.id)
		if Detalle_Perfil.objects.filter(Usuario=request.user).count() > 0:
			diccionario['dPerfil']=Detalle_Perfil.objects.get(Usuario=request.user)
		diccionario['marcas']=Marca.objects.all()
		diccionario['destacados']= images_destacados()
		diccionario['ofertas']= images_ofertas()
		diccionario['novedades'] = images_novedades()
		diccionario['detalle_img']= Detalle_Imagen.objects.all()
		return render_to_response('editar-perfil.html', diccionario, context_instance=RequestContext(request))

def actualizar_perfil(request):
	if not request.user.is_anonymous():
		if request.method=='POST':
			nombre=request.POST['Nombre']
			apellido=request.POST['Apellido']
			email=request.POST['Correo']
			usuario=request.POST['Usuario']
			telefono=request.POST['Telefono']
			direccion=request.POST['Direccion']

			u=User.objects.get(pk=request.user.id)
			d=Detalle_Perfil.objects.get(Usuario=request.user)

			u.first_name=nombre
			u.last_name=apellido
			u.email=email
			u.username=usuario
			d.Telefono=telefono
			d.Direccion=direccion
			u.save()
			d.save()

		return HttpResponseRedirect('/perfil-usuario/')
	else:
		return HttpResponseRedirect('/ingresar/')

def editar_contrasena(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
		diccionario['marcas']=Marca.objects.all()
		diccionario['destacados']= Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')[:2]
		diccionario['ofertas']= Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')[:2]
		diccionario['novedades'] = Producto.objects.filter(Fecha__month=datetime.now().month).order_by('?')[:2]
		diccionario['detalle_img']= Detalle_Imagen.objects.all()
	return render_to_response('editar-contrasena.html', diccionario, context_instance=RequestContext(request))

def actualizar_contrasena(request):
	error=0
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')[:2]
	diccionario['ofertas']= Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')[:2]
	diccionario['novedades'] = Producto.objects.filter(Fecha__month=datetime.now().month).order_by('?')[:2]
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		usuario=User.objects.get(pk=request.user.id)
		if request.method=='POST':
			cNueva=request.POST['cNueva']
			usuario.set_password(cNueva)
			usuario.save()
			return HttpResponseRedirect('/perfil-usuario/')
	else:
		return HttpResponseRedirect('/ingresar/')

def historial_compra(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')[:2]
	diccionario['ofertas']= Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')[:2]
	diccionario['novedades'] = Producto.objects.filter(Fecha__month=datetime.now().month).order_by('?')[:2]
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
		diccionario['compras']=Orden.objects.all()
	return render_to_response('historial-compra.html',diccionario, context_instance=RequestContext(request))
	
def detalle_compra(request, id_orden):
	precio=0
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')[:2]
	diccionario['ofertas']= Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')[:2]
	diccionario['novedades'] = Producto.objects.filter(Fecha__month=datetime.now().month).order_by('?')[:2]
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	orden = get_object_or_404(Orden, pk=id_orden)
	diccionario['orden']=orden
	detalle=Detalle_Carrito.objects.filter(Carrito=orden.Carrito)
	for item in detalle:
		precio += item.Producto.Precio * item.Cantidad
	Tot=precio
	diccionario['detalle']=detalle
	diccionario['Tot']=Tot
	return render_to_response('detalle-compra.html', diccionario, context_instance=RequestContext(request))

def historial_credito(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')[:2]
	diccionario['ofertas']= Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')[:2]
	diccionario['novedades'] = Producto.objects.filter(Fecha__month=datetime.now().month).order_by('?')[:2]
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
		diccionario['creditos']=Credito.objects.all().order_by('Fecha')
	return render_to_response('historial-credito.html', diccionario, context_instance=RequestContext(request))

def detalle_credito(request, id_credito):
	precio=0
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')[:2]
	diccionario['ofertas']= Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')[:2]
	diccionario['novedades'] = Producto.objects.filter(Fecha__month=datetime.now().month).order_by('?')[:2]
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	credito = get_object_or_404(Credito, pk=id_credito)
	diccionario['pagos']=Pagos.objects.filter(Credito=credito)
	diccionario['credito']=credito
	return render_to_response('detalle-credito.html', diccionario, context_instance=RequestContext(request))
#Vista para verificar el Usuario a registrar--Ajax
def verificar_usuario(request):
	if request.is_ajax():
		if request.method=='POST':
			user=request.POST['usuario']
			cUser=User.objects.filter(username=user).count()
			if cUser >=1:
				tUser=1
			else:
				tUser=0
	return HttpResponse(json.dumps({'tUser':tUser}), content_type='application/json')

#Vista para verificar el email a registrar--Ajax
def verificar_email(request):
	if request.is_ajax():
		if request.method=='POST':
			email=request.POST['email']
			cUser=User.objects.filter(email=email).count()
			if cUser >=1:
				tUser=1
			else:
				tUser=0
	return HttpResponse(json.dumps({'tUser':tUser}), content_type='application/json')

def verificar_rnp(request):
	if request.is_ajax():
		if request.method=='POST':
			rnp=request.POST['rnp']
			cUser=Detalle_Perfil.objects.filter(RNP=rnp).count()
			if cUser >=1:
				tUser=1
			else:
				tUser=0
	return HttpResponse(json.dumps({'tUser':tUser}), content_type='application/json')

def cargar_region(request):
	if request.is_ajax():
		if request.method=='POST':
			pais = request.POST['pais']
			region = Region.objects.filter(Pais=Pais.objects.get(pk=pais))
	return render_to_response('cargar-combo.html', {'datos':region, 'r':True},context_instance=RequestContext(request))

def cargar_ciudad(request):
	if request.is_ajax():
		if request.method=='POST':
			region = request.POST['region']
			ciudad = Ciudad.objects.filter(Region=Region.objects.get(pk=region))
	return render_to_response('cargar-combo.html', {'datos':ciudad, 'c':True},context_instance=RequestContext(request))

def contactanos(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')[:2]
	diccionario['ofertas']= Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')[:2]
	diccionario['novedades'] = Producto.objects.filter(Fecha__month=datetime.now().month).order_by('?')[:2]
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	diccionario['contactos']= Contactos.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	return render_to_response('contactanos.html', diccionario, context_instance=RequestContext(request))

def cargar_imagen(request):
	formulario = CargarImagenForm()
	return render_to_response('cargar_imagen_producto.html',{'form':formulario},context_instance=RequestContext(request))

def faq(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')[:2]
	diccionario['ofertas']= Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')[:2]
	diccionario['novedades'] = Producto.objects.filter(Fecha__month=datetime.now().month).order_by('?')[:2]
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	diccionario['preguntas']=FAQ.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	return render_to_response('faq.html',diccionario,context_instance=RequestContext(request))

def mision_vision(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')[:2]
	diccionario['ofertas']= Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')[:2]
	diccionario['novedades'] = Producto.objects.filter(Fecha__month=datetime.now().month).order_by('?')[:2]
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	return render_to_response('mision_vision.html', diccionario,context_instance=RequestContext(request))

def politica(request):
	diccionario={}
	diccionario['marcas']=Marca.objects.all()
	diccionario['destacados']= Producto.objects.filter(Destacado__exact=True, Oferta__exact=False).order_by('?')[:2]
	diccionario['ofertas']= Producto.objects.filter(Destacado__exact=False, Oferta__exact=True).order_by('?')[:2]
	diccionario['novedades'] = Producto.objects.filter(Fecha__month=datetime.now().month).order_by('?')[:2]
	diccionario['detalle_img']= Detalle_Imagen.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user
		diccionario['centinela']=True
	return render_to_response('politica.html', diccionario,context_instance=RequestContext(request))

