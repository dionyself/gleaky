from graphene import ObjectType
from .asset import CreateAsset
from .asset import UpdateAsset
from .asset_tag import CreateAssetTag
from .asset_tag import UpdateAssetTag
from .invoice import CreateInvoice
from .invoice import UpdateInvoice


class Mutation(ObjectType):
    create_asset = CreateAsset.Field()
    update_asset = UpdateAsset.Field()
    create_asset_tag = CreateAssetTag.Field()
    update_asset_tag = UpdateAssetTag.Field()
    create_invoice = CreateInvoice.Field()
    update_invoice = UpdateInvoice.Field()
