import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from warehouses.models import Asset
from graphene.types.generic import GenericScalar


class AssetNode(DjangoObjectType):
    properties = GenericScalar()
    duration = graphene.String()

    class Meta:
        model = Asset
        interfaces = (relay.Node, )
        exclude_fields = ["is_deleted"]
        #only_fields = ["created_at"]
        filter_fields = {
            "starts_at": ["lte", "gte", "gt", "lt"],
        }
