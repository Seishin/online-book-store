from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'web_site.views.homePage'),
    url(r'^page/(?P<page>\d+)/$', 'web_site.views.homePage'),

    url(r'^basket/page/(\d+)/$', 'web_site.views.basketPage'),
    url(r'^page/(?P<page>\d+)/order/(?P<ordered_by>[a-zA-Z0-9_.-]+)/$', 'web_site.views.homePage'),

    url(r'^category/(?P<chosen_category>\d+)/page/(?P<page>\d+)/$', 'web_site.views.categoryPage'),
    url(r'^category/(?P<chosen_category>\d+)/page/(?P<page>\d+)/order/(?P<ordered_by>\w+)/$', 'web_site.views.categoryPage'),

    url(r'^register/$', 'web_site.views.registerPage'),
    url(r'^registerUser/$', 'web_site.views.register'),

    url(r'^buy/(\d+)/$', 'web_site.views.buyABook'),
    url(r'^unbuy/(\d+)/$', 'web_site.views.unbuyABook'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^assets/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

    url(r'^login/$', 'web_site.views.login'),
    url(r'^logout/$', 'web_site.views.logout'),
)
