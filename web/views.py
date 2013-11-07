# -*- coding:utf-8 -*-
from web.models import Producto, Categoria, SubCategoria, Marca
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

#Vista que retorna la pagina de inicio
def inicio(request):
	return render_to_response('index.html', context_instance=RequestContext(request))

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

		