from django.core.paginator import Paginator
from . import keys

def apply_pagination(queryset, page=1, total_entities=10):
    paginator = Paginator(queryset, per_page=total_entities)
    data = {}
    total_page = paginator.num_pages
    data[keys.TOTAL_PAGES] = total_page
    if total_page < int(page):
        page = total_page
    data[keys.PAGE] = page
    queryset = paginator.get_page(page)
    return queryset, data