import graphene

from ingredients.schema import IngredientsQuery


class Query(IngredientsQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass 



schema = graphene.Schema(query=Query)