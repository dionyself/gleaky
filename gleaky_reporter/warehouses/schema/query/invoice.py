from graphene_django import DjangoObjectType
from graphene import relay
from warehouses.models import Invoice
from graphene.types.generic import GenericScalar


class InvoiceNode(DjangoObjectType):
    properties = GenericScalar()

    class Meta:
        model = Invoice
        interfaces = (relay.Node, )
        exclude_fields = ["is_deleted"]
        #only_fields = ["created_at"]
        filter_fields = {
            "created_at": ["lte", "gte", "gt", "lt"],
        }
