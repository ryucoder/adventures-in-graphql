# import graphene
# from graphene_django import DjangoObjectType

# from ingredients.models import Category, Ingredient


# class CategoryType(DjangoObjectType):
#     class Meta:
#         model = Category
#         fields = ("id", "name", "ingredients")


# class IngredientType(DjangoObjectType):
#     class Meta:
#         model = Ingredient
#         fields = ("id", "name", "notes", "category")


# class Query(graphene.ObjectType):
#     all_ingredients = graphene.List(IngredientType)
#     category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

#     def resolve_all_ingredients(root, info):
#         # We can easily optimize query count in the resolve method
#         return Ingredient.objects.select_related("category").all()

#     def resolve_category_by_name(root, info, name):
#         try:
#             return Category.objects.get(name=name)
#         except Category.DoesNotExist:
#             return None



import graphene 

from graphene import relay
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django.filter import DjangoFilterConnectionField

from ingredients.models import Category, Ingredient

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")


# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node, )


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node, )


class IngredientsQuery(graphene.ObjectType):
    all_category = DjangoListField(CategoryType)

    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)


# schema = graphene.Schema(query=IngredientsQuery)