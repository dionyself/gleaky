import graphene
from warehouses.models import AssetTag, Asset
from graphene.types.generic import GenericScalar


class CreateAssetTag(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()
        tag_type = graphene.String()
        priority = graphene.Int()
        properties = GenericScalar()
        assets = graphene.List(graphene.Int)
        is_deleted = graphene.Boolean()
        is_disabled = graphene.Boolean()

    tag_id = graphene.Int()
    ok = graphene.Boolean()
    tagged_assets = graphene.List(graphene.Int)
    failed_assets = graphene.List(graphene.Int)

    def mutate(self, info, **args):

        ok = False
        assets = args.pop('assets', [])

        try:
            tag = AssetTag.objects.create(**args)
            ok = True
        except:
            tag = None

        tagged_assets = []
        failed_assets = []
        for asset_id in assets:
            try:
                tag.assets.add(Asset.objects.filter(
                    id=asset_id).first())
                tagged_assets.append(asset_id)
            except:
                failed_assets.append(asset_id)
                ok = False

        return CreateAssetTag(
            tag_id=tag and tag.id or 0,
            failed_assets=failed_assets,
            tagged_assets=tagged_assets,
            ok=ok)


class UpdateAssetTag(graphene.Mutation):
    class Arguments:
        pk = graphene.Int()
        name = graphene.String()
        description = graphene.String()
        tag_type = graphene.String()
        priority = graphene.Int()
        properties = GenericScalar()
        assets_to_tag = graphene.List(graphene.Int)
        assets_to_untag = graphene.List(graphene.Int)
        is_deleted = graphene.Boolean()
        is_disabled = graphene.Boolean()

    tag_id = graphene.Int()
    ok = graphene.Boolean()
    tagged_assets = graphene.List(graphene.Int)
    untagged_assets = graphene.List(graphene.Int)
    failed_assets = graphene.List(graphene.Int)

    def mutate(self, info, **args):

        ok = False
        tag = None
        assets_to_tag = args.pop('assets_to_tag', [])
        assets_to_untag = args.pop('assets_to_untag', [])

        try:
            if 'pk' in args:
                pk = args.pop("pk")
                AssetTag.objects.filter(id=pk).update(**args)
                tag = AssetTag.objects.filter(id=pk).first()
                ok = True
        except:
            tag = None

        tagged_assets = []
        untagged_assets = []
        failed_assets = []
        for asset_id in assets_to_tag:
            try:
                tag.assets.add(Asset.objects.filter(
                    id=asset_id).first())
                tagged_assets.append(asset_id)
            except:
                failed_assets.append(asset_id)
                ok = False
        for asset_id in assets_to_untag:
            try:
                tag.assets.remove(Asset.objects.filter(
                    id=asset_id).first())
                untagged_assets.append(asset_id)
            except:
                failed_assets.append(asset_id)
                ok = False

        return UpdateAssetTag(
            tag_id=tag and tag.id or 0,
            failed_assets=failed_assets,
            tagged_assets=tagged_assets,
            untagged_assets=untagged_assets,
            ok=ok)
