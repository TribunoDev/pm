#-*- coding:utf-8 -*-
from web.models import *
from django.contrib import admin

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Orden)
admin.site.register(Estado)
admin.site.register(Carrito)
admin.site.register(Detalle_Carrito)
admin.site.register(Direccion_Orden)
admin.site.register(Pais)
admin.site.register(Region)
admin.site.register(Marca)
admin.site.register(Detalle_Perfil)
admin.site.register(Detalle_Imagen)
admin.site.register(Servicio_Flete)
admin.site.register(Precio_Combustible)
admin.site.register(Orden_Estado)
admin.site.register(Credito)
admin.site.register(Pagos)