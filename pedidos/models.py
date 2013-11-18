#encoding:utf-8
from django.db import models
from datetime import datetime

class pedidos(models.Model):
	IdPedido = models.AutoField(primary_key=True)
	NumPedidoDiario = models.IntegerField(help_text='Número de Pedido', verbose_name=u'Pedido')
	NumFactura = models.IntegerField(help_text='Número de Factura', verbose_name=u'Factura')
	IdEstado = models.IntegerField(help_text='Estado del Pedido', verbose_name=u'Estado')
	ComentarioConserje = models.TextField(max_length=500, help_text='Comentario del Conserje', verbose_name=u'Comentario')
	FechaHoraEntrega = models.DateTimeField(auto_now_add=True, help_text='Fecha y Hora de Entrega', verbose_name=u'Entregado')
	Latitud = models.CharField(max_length=50, help_text='Latitud', verbose_name=u'Latitud')
	Longitud = models.CharField(max_length=50, help_text='Longitud', verbose_name=u'Longitud')

	def __unicode__(self):
		return 'Pedido # ' + self.NumPedidoDiario + ' - Factura: ' self.NumFactura