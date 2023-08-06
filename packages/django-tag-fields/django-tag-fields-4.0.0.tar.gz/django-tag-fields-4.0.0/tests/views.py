from django.views.generic.list import ListView

from tag_fields.views import TagListMixin

from .models import Food


class FoodTagListView(TagListMixin, ListView):
    model = Food
