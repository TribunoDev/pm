#encoding:utf-8
from django.db import models
from datetime import datetime

class Pedido(models.Model):
	IdPedido = models.AutoField(primary_key=True)
	NumPedidoDiario = models.IntegerField(help_text='Número de Pedido', verbose_name=u'Pedido')
	NumFactura = models.CharField(max_length=25, help_text='Número de Factura', verbose_name=u'Factura')
	IdEstado = models.IntegerField(help_text='Estado del Pedido', verbose_name=u'Estado')
	ComentarioConserje = models.TextField(max_length=500, help_text='Comentario del Conserje', verbose_name=u'Comentario', null=True, blank=True)
	FechaHoraEntrega = models.DateTimeField(auto_now_add=True, help_text='Fecha y Hora de Entrega', verbose_name=u'Entregado', null=True, blank=True)
	Entregado = models.BooleanField(help_text='Entregado', verbose_name=u'Entregado')
	Latitud = models.CharField(max_length=50, help_text='Latitud', verbose_name=u'Latitud', null=True, blank=True)
	Longitud = models.CharField(max_length=50, help_text='Longitud', verbose_name=u'Longitud', null=True, blank=True)
	Sincronizar = models.BooleanField(help_text='Debo sincronizarlo?', verbose_name=u'Sincronizar')

	def __unicode__(self):
		return 'Pedido # ' + str(self.NumPedidoDiario) + ' - Factura: ' + str(self.NumFactura)