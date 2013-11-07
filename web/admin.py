#-*- coding:utf-8 -*-
from web.models import Producto, Categoria, SubCategoria, Orden, Estado_Orden, Detalle_Orden, Direccion_Orden, Pais, Marca
from django.contrib import admin

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Orden)
admin.site.register(Estado_Orden)
admin.site.register(Detalle_Orden)
admin.site.register(Direccion_Orden)
admin.site.register(Pais)
admin.site.register(Marca)
