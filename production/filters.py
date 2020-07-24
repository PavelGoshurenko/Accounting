import django_filters
from production.models import Ingredient


class IngredientFilter(django_filters.FilterSet):
    class Meta:
        model = Ingredient
        fields = ['category']