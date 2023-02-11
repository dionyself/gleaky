from graphene import Field, relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene.types.generic import GenericScalar
from graphene_django.debug import DjangoDebug
from django.conf import settings
from .asset import AssetNode
from .asset_tag import AssetTagNode
from .invoice import InvoiceNode


class Query(ObjectType):

    asset = relay.Node.Field(AssetNode)
    assets = DjangoFilterConnectionField(AssetNode)

    asset_tag = relay.Node.Field(AssetTagNode)
    asset_tags = DjangoFilterConnectionField(AssetTagNode)

    invoice = relay.Node.Field(InvoiceNode)
    invoices = DjangoFilterConnectionField(InvoiceNode)

    debug = Field(DjangoDebug, name='__debug')

    about = GenericScalar()

    def resolve_about(self, info, **args):
        return {
            "API version": settings.LEAKY_VERSION}
