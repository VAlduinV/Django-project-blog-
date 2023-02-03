from django.db.models import Count
from django.core.cache import cache
from .models import *

menu = [{'title': "Про нас", 'url_name': 'about'},
        {'title': "Додати статтю", 'url_name': 'add_page'},
        {'title': "Контакти", 'url_name': 'contact'},
]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        techs = cache.get('techs')
        if not techs:
            techs = Category.objects.annotate(Count('main'))
            cache.set('techs', techs, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = techs
        if 'tech_selected' not in context:
            context['cat_selected'] = 0
        return context
