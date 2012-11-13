__author__ = 'seishin'

from django.contrib import admin
from web_site.models import *

admin.site.register(Categories)
admin.site.register(Books)
admin.site.register(Authors)
admin.site.register(Purchases)

