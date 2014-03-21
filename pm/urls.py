from web.models import *
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
   # url(r'^currencies/', include('currencies.urls')),

    url(r'^$', 'web.views.inicio', name='inicio'),
    url(r'^actualizar-cantidad/$', 'web.views.actualizar_cantidad', name='actualizar_cantidad'),
    url(r'^actualizar-contrasena/$', 'web.views.actualizar_contrasena', name='actualizar_contrasena'),
    url(r'^actualizar-perfil/$', 'web.views.actualizar_perfil', name='actualizar_perfil'),
    url(r'^buscar/$', 'web.views.buscar', name='buscar'),
    url(r'^agregar-carrito/$', 'web.views.agregar_carrito', name='agregar_carrito'),
    url(r'^catalogo-productos/$', 'web.views.catalogo_productos', name='catalogo_productos'),
    url(r'^cargar-imagen/$', 'web.views.cargar_imagen', name='cargar_imagen'),
    url(r'^carrito/$', 'web.views.carrito', name='carrito'),
    url(r'^contactanos/$', 'web.views.contactanos', name='contactanos'),
    url(r'^datos-carrito/$', 'web.views.datos_carrito', name='datos_carrito'),
    url(r'^detalle-compra/(?P<id_orden>\d+)/$', 'web.views.detalle_compra', name='detalle_compra'),
    url(r'^detalle-credito/(?P<id_credito>\d+)/$', 'web.views.detalle_credito', name='detalle_credito'),
    url(r'^destacados/$', 'web.views.productos_destacados', name='productos_destacados'),
    url(r'^editar-perfil/$', 'web.views.editar_perfil', name='editar_perfil'),
    url(r'^editar-contrasena/$', 'web.views.editar_contrasena', name='editar_contrasena'),
    url(r'^enviar-email/$', 'web.views.enviar_email', name='enviar_email'),
    url(r'^enviar-datos-pago/$', 'web.views.envio_datos_pago', name='envio_datos_pago'),
    url(r'^enviar-direccion/$', 'web.views.envio_direccion', name='envio_direccion'),
    url(r'^enviar-pago/$', 'web.views.envio_pago', name='envio_pago'),
    url(r'^enviar-pago-carrito/$', 'web.views.envio_pago_directo', name='envio_pago_directo'),
    url(r'^faq/$', 'web.views.faq', name='faq'),
    url(r'^resultado-transaccion/$', 'web.views.procesar_pago', name='procesar_pago'),
    url(r'^form-editar-cantidad/$', 'web.views.form_editar_cantidad', name='form_editar_cantidad'),
    url(r'^guardar-direccion/$', 'web.views.guardar_direccion', name='guardar_direccion'),
    url(r'^detalle-producto/(?P<id_producto>\d+)/$', 'web.views.detalle_producto', name='detalle_producto'),
    url(r'^home/$', 'web.views.home', name='home'),
    url(r'^historial-de-compra/$', 'web.views.historial_compra', name='historial_compra'),
    url(r'^historial-de-credito/$', 'web.views.historial_credito', name='historial_credito'),
    url(r'^ingresar/$', login, {'template_name': 'inicio-sesion.html',}, name='login'),
    url(r'^marcas/$', 'web.views.marcas', name='marcas'),
    url(r'^marcas/(?P<id_marca>\d+)/$', 'web.views.marca_producto', name='marca_producto'),
    url(r'^mision_vision/$', 'web.views.mision_vision', name='mision_vision'),
    url(r'^ofertas/$', 'web.views.productos_ofertas', name='productos_ofertas'),
    url(r'^perfil-usuario/$', 'web.views.perfil_usuario', name='perfil_usuario'),
    url(r'^politica/$', 'web.views.politica', name='politica'),
    url(r'^productos-en-oferta/$', 'web.views.ofertas', name='ofertas'),
    url(r'^productos-destacados/$', 'web.views.destacados', name='destacados'),
    url(r'^productos-en-novedades/$', 'web.views.novedades', name='novedades'),
    url(r'^productos/categoria/subcategoria/(?P<id_subcat>\d+)$', 'web.views.ver_subcategoria', name='ver_subcategoria'),
    #url(r'^procesar-pago/$', 'web.views.procesar_pago', name='procesar_pago'),
    #url(r'^recuperar-contrasena/$', 'web.views.recuperar_contrasena', name='recuperar_contrasena'),
    url(r'^registro/$', 'web.views.registrar', name='registrar'),
    url(r'^registrado/$', 'web.views.registrado', name='registrado'),
    url(r'^salir/$', logout,{'template_name': 'index.html',}, name='logout'),
    url(r'^servicio-flete/$', 'web.views.servicio_flete', name='servicio_flete'),


    #prueba
    url(r'^user/password/reset$', password_reset,{'template_name': 'password_reset_form.html','post_reset_redirect': '/user/password/reset/done/'}, name='password_reset'),
    url(r'^user/password/reset/done/$', password_reset_done,{'template_name': 'password_reset_done.html'},name='password_reset_done'),
    url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,{'template_name': 'password_reset_email.html', 'post_reset_redirect': '/user/password/done/'}, name='password_reset_confirm'),
    url(r'^user/password/done/$', password_reset_complete,{'template_name': 'password_reset_complete.html'},name='password_reset_complete'),
    #

    #URL'S AJAX---
    url(r'^cargar-ciudad/$', 'web.views.cargar_ciudad', name='cargar_ciudad'),
    url(r'^cargar-region/$', 'web.views.cargar_region', name='cargar_region'),
    url(r'^eliminar-item/$', 'web.views.eliminar_item_detalle', name='eliminar_item_detalle'),
    url(r'^item-carrito/$', 'web.views.item_carrito', name='item_carrito'),
    url(r'^obtener-datos-carrito/$', 'web.views.items_en_carrito', name='items_en_carrito'),
    url(r'^obtener-info-usuario/$', 'web.views.info_usuario', name='info_usuario'),
    url(r'^verificar-usuario/$', 'web.views.verificar_usuario', name='verificar_usuario'),
    url(r'^verificar-email/$', 'web.views.verificar_email', name='verificar_email'),
    url(r'^verificar-rnp/$', 'web.views.verificar_rnp', name='verificar_rnp'),

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
