__author__ = 'seishin'

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginator(recs, page):
    # Paginator config
    paginator = Paginator(recs, 5)

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        records = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        records = paginator.page(paginator.num_pages)

    return records