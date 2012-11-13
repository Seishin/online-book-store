__author__ = 'seishin'

from django.db import models
from django.utils.encoding import force_unicode
from django.contrib import auth

class Categories(models.Model):
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return force_unicode(self.name)

class Books(models.Model):
    title        = models.CharField(max_length = 50)
    annotation   = models.TextField()
    category     = models.ForeignKey('Categories')
    author       = models.ForeignKey('Authors')
    pub_date     = models.DateTimeField()
    price        = models.DecimalField(max_digits = 5, decimal_places = 2)
    cover_img    = models.CharField(max_length = 250)

    def __unicode__(self):
        return force_unicode(self.title)

class Authors(models.Model):
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return force_unicode(self.name)

class Purchases(models.Model):
    book            = models.ForeignKey('Books')
    user            = models.ForeignKey(auth.models.User)
    purchase_date   = models.DateField()

    def __unicode__(self):
        return force_unicode(self.book)
