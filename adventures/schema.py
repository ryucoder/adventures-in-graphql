import graphene

from graphene_django.debug import DjangoDebug

from ingredients.schema import IngredientsQuery


class Query(IngredientsQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query)