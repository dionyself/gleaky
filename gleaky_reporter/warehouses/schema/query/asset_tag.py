from graphene_django import DjangoObjectType
from graphene import relay
from warehouses.models import AssetTag
from graphene.types.generic import GenericScalar


class AssetTagNode(DjangoObjectType):
    properties = GenericScalar()

    class Meta:
        model = AssetTag
        interfaces = (relay.Node, )
        exclude_fields = ["is_deleted"]
        #only_fields = ["created_at"]
        filter_fields = {
            "created_at": ["lte", "gte", "gt", "lt"],
        }
