#-*- coding:utf-8 -*-
from web.models import Producto, Categoria, SubCategoria, Orden
from django.contrib import admin

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Orden)
