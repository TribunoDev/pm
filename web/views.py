# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from web.models import Producto, Categoria, SubCategoria, Marca
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from web.forms import SignUpForm

#Vista que retorna la pagina de inicio
def inicio(request):
	return render_to_response('index.html', context_instance=RequestContext(request))


def home(request):
	return render_to_response('home.html', {'usuario': request.user}, context_instance=RequestContext(request))

#Vista que retorna la ventana de inicio de sesion
def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/privado')

	if request.method=='POST':
		frmSesion = AuthenticationForm(request.POST)
		if frmSesion.is_valid():
			usuario = request.POST["username"]
			clave = request.POST["password"]
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/privado')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request))
	else:
		frmSesion = AuthenticationForm()
	return render_to_response('inicio-sesion.html',{'frmSesion': frmSesion}, context_instance=RequestContext(request))

@login_required(LOGIN_URL = '/ingresar')
def privado(request):
	usuario = request.user
	return render_to_response('privado.html', {'usuario': usuario}, context_instance=RequestContext(request))

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

			return HttpResponseRedirect(reverse('inicio'))
	else:
		frmUser = SignUpForm()

	return render_to_response('registro.html', {'frmUser': frmUser}, context_instance=RequestContext(request))

#Vista que devuelve las marcas de los productos
def marcas(request):
	marca = Marca.objects.all()
	return render_to_response('marcas.html', {'marcas': marca}, context_instance=RequestContext(request))

#Vista que retorna los productos por cada marca
def marca_producto(request, id_marca):
	marca = get_object_or_404(Marca, pk=id_marca)
	productos = Producto.objects.filter(Descripcion__icontains=marca)
	return render_to_response('productos-marcas.html', {'marca':marca, 'productos':productos}, context_instance=RequestContext(request))

#Vista para devolver los productos con categoria "Novedades"
def destacados(request):
	destacados = Producto.objects.filter(Destacado__exact=True)
	return render_to_response('productos-en-oferta.html', {'datos': destacados}, context_instance= RequestContext(request))

#Vista que devuelve los productos que estan en la categoria de Ofertas
def ofertas(request):
	ofertas = Producto.objects.filter(Oferta__exact=True)
	return render_to_response('productos-en-oferta.html', {'datos':ofertas}, context_instance=RequestContext(request))

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
	return render_to_response('productos-subcategoria.html', {'datos':subcat ,'productos': productos}, context_instance=RequestContext(request))

def detalle_producto(request):
	if request.method=='POST':
		id_producto = request.POST["parametro"]
		detalle = Producto.objects.get(Codigo__contains=id_producto)
	return render_to_response('detalle-producto.html', {'detalle':detalle}, context_instance=RequestContext(request))

		