__author__ = 'seishin'

from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from web_site.models import *
from django.conf import settings
from widgets.paginator import paginator
from django.contrib.auth.models import User
from django.http import HttpResponse
from datetime import datetime

def homePage(request, page = '1', ordered_by = 'pub_date'):
    purchased_books = 0

    books = paginator(Books.objects.all().order_by(ordered_by), page)

    if request.user.is_authenticated():
        purchased_books = Purchases.objects.filter(user = request.user).count()

    data = {'categories' : Categories.objects.all().order_by('name'),
            'books' : books,
            'purchased_books' : purchased_books,
            'url' : settings.URL,
            'ordered_by' : ordered_by }

    return direct_to_template(request, 'homepage.html', data)

def categoryPage(request, chosen_category = None, page = '1', ordered_by = 'pub_date'):
    books = paginator(Books.objects.filter(category = chosen_category).order_by(ordered_by), page)
    purchased_books = 0

    if request.user.is_authenticated():
        purchased_books = Purchases.objects.filter(user = request.user).count()

    data = {'categories' : Categories.objects.all().order_by('name'),
            'books' : books,
            'purchased_books' : purchased_books,
            'url' : settings.URL,
            'category' : chosen_category,
            'ordered_by' : ordered_by }

    return direct_to_template(request, 'books.html', data)

def basketPage(request, page = 1):
    """
    The function for the basket page.
    It checks whether the user who opened it is already authenticated or not.
    If it's then shows all the purchased books and provides simple information
    about how much money is needed to be paid for how many books.
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    purchased_books = Purchases.objects.filter(user = request.user)

    books = paginator(purchased_books, page)

    money = 0

    for book in purchased_books:
        money += book.book.price

    data = {'books' : books,
        'purchased_books' : purchased_books.count(),
        'money' : money,
        'url' : settings.URL }

    return direct_to_template(request, 'basket.html', data)

def registerPage(request):
    """
    Register page rending function.
    Checks whether the user is already authenticated and if it's redirects
    to the home page.
    """

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    data = {'url' : settings.URL}

    return direct_to_template(request, 'register.html', data)

def register(request):
    """
    The registration logics function and rendiring page.
    Checks whether the user is already authenticated and if it's redirects to the
    home page.
    It gets username, password and email records from the form via POST request.
    Then makes a simple checks whether all the information is provided and
    if everything is okay then creates the new user and redirects to the home page.
    """

    username    = request.POST.get('inputUsername', '')
    password    = request.POST.get('inputPassword', '')
    email       = request.POST.get('inputEmail', '')

    data = {'url' : settings.URL,
            }

    if username and password and email:
        if not User.objects.filter(username = username):
            user = User.objects.create_user(username, email, password)
            user.is_alive = True
            user.save()

            return HttpResponseRedirect('/')
        else:
            return direct_to_template(request, 'error.html', {'error' : 'Username is already used!',
                                                              'url' : settings.URL})
    else:
        return direct_to_template(request, 'error.html', {'error' : 'Wrong entered data!',
                                                          'url' : settings.URL,
                                                          'page' : 'register/'})

def buyABook(request, book_id = None):
    """
    When a book is purchased it's available in the Basket page.
    The function takes the book_id and creates a new purchase.
    """

    purchased_book = Purchases(book = Books.objects.get(pk = int(book_id)), user = request.user, purchase_date = datetime.now())
    purchased_book.save()

    return HttpResponseRedirect(settings.URL + '/basket/page/1')

def unbuyABook(request, purchase_id):
    """
    When book is bought via this function is removed from the basket.
    """

    purchased_book = Purchases(pk = purchase_id).delete()

    return HttpResponseRedirect(settings.URL + '/basket/page/1')

def login(request):
    """
    Authenticate users and redirect them to the home page.
    If there is an error shows a message.
    """

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username = username, password = password)

    if user is not None and user.is_active:
        auth.login(request, user)

        return HttpResponseRedirect('/')
    else:
        return direct_to_template(request, 'error.html', {'error' : 'Wrong username or password!',
                                                          'url' : settings.URL,
                                                          'page' : ''})

def logout(request):
    """
    Log users out and re-direct them to the main page.
    """

    auth.logout(request)

    return HttpResponseRedirect('/')