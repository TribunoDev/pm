# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from pedidos.models import Pedido
from datetime import datetime
from django.core import serializers
from pedidos.forms import EntregaForm
from datetime import datetime

def EntregaProducto(request, NumFact):
	dato = get_object_or_404(Pedido, NumFactura=NumFact)
	Filtro = Pedido.objects.filter(NumFactura=NumFact)
	return render_to_response('entregarProducto.html', {'PedidoFiltrado' : dato}, context_instance=RequestContext(request))

def ActualizarEntrega(request):
	if request.method == 'POST':
		if request.POST.get('Entregado', False):
			vEntregado = True
		else:
			vEntregado = False
		vSincronizar = True
		vAhorita = datetime.datetime.now()
		
		Pedido.objects.filter(NumFactura=request.POST['NumFactura']).update(ComentarioConserje=request.POST['ComentarioConserje'], Entregado=vEntregado, Latitud=request.POST['Latitud'], Longitud=request.POST['Longitud'], Sincronizar=vSincronizar, FechaHoraEntrega=vAhorita)
		return render_to_response('graciasEntregado.html', context_instance=RequestContext(request))