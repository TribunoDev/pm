from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.conf import settings
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.inicio', name='inicio'),
    url(r'^actualizar-cantidad/$', 'web.views.actualizar_cantidad', name='actualizar_cantidad'),
    url(r'^buscar/$', 'web.views.buscar', name='buscar'),
    url(r'^agregar-carrito/$', 'web.views.agregar_carrito', name='agregar_carrito'),
    url(r'^catalogo-productos/$', 'web.views.catalogo_productos', name='catalogo_productos'),
    url(r'^carrito/$', 'web.views.carrito', name='carrito'),
    url(r'^datos-carrito/$', 'web.views.datos_carrito', name='datos_carrito'),
    url(r'^form-editar-cantidad/$', 'web.views.form_editar_cantidad', name='form_editar_cantidad'),
    url(r'^detalle-producto/(?P<id_producto>\d+)/$', 'web.views.detalle_producto', name='detalle_producto'),
    url(r'^home/$', 'web.views.home', name='home'),
    url(r'^ingresar/$', login, {'template_name': 'inicio-sesion.html',}, name='login'),
    url(r'^item-carrito/$', 'web.views.item_carrito', name='item_carrito'),
    url(r'^marcas/$', 'web.views.marcas', name='marcas'),
    url(r'^marcas/(?P<id_marca>\d+)/$', 'web.views.marca_producto', name='marca_producto'),
    url(r'^productos-en-oferta/$', 'web.views.ofertas', name='ofertas'),
    url(r'^productos-destacados/$', 'web.views.destacados', name='destacados'),
    url(r'^productos/categoria/subcategoria/(?P<id_subcat>\d+)$', 'web.views.ver_subcategoria', name='ver_subcategoria'),
    url(r'^salir/$', logout,{'template_name': 'index.html',}, name='logout'),
    url(r'^registro/$', 'web.views.registrar', name='registrar'),
    url(r'^registrado/$', 'web.views.registrado', name='registrado'),

    #URL'S AJAX---
    url(r'^eliminar-item/$', 'web.views.eliminar_item_detalle', name='eliminar_item_detalle'),
    #---URL'S AJAX

    # url(r'^pm/', include('pm.foo.urls')),
    
    #App de pedidos -->
    url(r'EntregaDomicilio/(?P<NumFact>\d+)/$', 'pedidos.views.EntregaProducto', name='EntregaProducto'),
    url(r'GuardarPedido/$', 'pedidos.views.ActualizarEntrega', name='ActualizarEntrega'),
    # <-- App de pedidos

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}, ),
)
