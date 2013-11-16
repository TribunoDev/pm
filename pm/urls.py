from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.inicio', name='inicio'),
    url(r'^ingresar/$', 'web.views.ingresar', name='ingresar'),

    url(r'^ingresar/$', 'web.views.ingresar', name='ingresar'),
    url(r'^registro/$', 'web.views.registrar', name='registrar'),
    url(r'^marcas/$', 'web.views.marcas', name='marcas'),
    url(r'^marcas/(?P<id_marca>\d+)/$', 'web.views.marca_producto', name='marca_producto'),
    url(r'^productos/categoria/subcategoria/(?P<id_subcat>\d+)$', 'web.views.ver_subcategoria', name='ver_subcategoria'),
    url(r'^productos-destacados/$', 'web.views.destacados', name='destacados'),
    url(r'^productos-en-oferta/$', 'web.views.ofertas', name='ofertas'),
    url(r'^catalogo-productos/$', 'web.views.catalogo_productos', name='catalogo_productos'),
    url(r'^detalle-producto/$', 'web.views.detalle_producto', name='detalle_producto'),

    # url(r'^pm/', include('pm.foo.urls')),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}, ),
)
