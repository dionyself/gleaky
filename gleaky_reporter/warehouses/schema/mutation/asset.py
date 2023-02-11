from django.utils import timezone
import graphene
from datetime import datetime, timedelta
from world.models import Product
from warehouses.models import Asset, AssetTag
from djmoney.money import Money
from graphene.types.generic import GenericScalar
from graphene.types.datetime import DateTime


class CreateAsset(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int()
        modded_product_name = graphene.String()
        cost = graphene.Int()
        existence = graphene.Int()
        properties = GenericScalar()
        tags = graphene.List(graphene.Int)
        asset_type = graphene.String()
        category = graphene.String()
        duration = graphene.String()
        expires_at = DateTime()
        starts_at = DateTime()
        is_deleted = graphene.Boolean()
        is_expired = graphene.Boolean()

    asset_id = graphene.Int()
    ok = graphene.Boolean()
    added_tags = graphene.List(graphene.Int)
    failed_tags = graphene.List(graphene.Int)

    def mutate(self, info, **args):

        ok = False
        asset = None
        tags = args.pop("tags", [])
        parsed_args = args.copy()
        if "product_id" in args:
            del parsed_args["product_id"]
        if "starts_at" not in args:
            parsed_args["starts_at"] = timezone.now()
        if "expires_at" in args:
            parsed_args["duration"] = args["expires_at"] - parsed_args["starts_at"]
        elif "duration" in args:
            t = datetime.strptime(args["duration"], "%d days, %H:%M:%S")
            parsed_args["duration"] = timedelta(
                days=t.day, hours=t.hour, minutes=t.minute, seconds=t.second)
            args["expires_at"] = parsed_args["starts_at"] + parsed_args["duration"]

        parsed_args.update(
            product=Product.objects.filter(
                id=args.get("product_id")).first() or None,
            cost=Money(args.get("cost", 0)),
        )

        if parsed_args["product"] or parsed_args.get("modded_product_name"):
            #  assets requires a product or modded_product_name to be created
            try:
                asset = Asset.objects.create(**parsed_args)
                ok = True
            except:
                ok = False

        added_tags = []
        failed_tags = []

        for tag_id in tags:
            try:
                tag = AssetTag.objects.get(pk=tag_id)
                asset.assettag_set.add(tag)
                added_tags.append(tag_id)
            except:
                failed_tags.append(tag_id)
                ok = False

        return CreateAsset(
            asset_id=asset and asset.id or 0,
            added_tags=added_tags,
            failed_tags=failed_tags,
            ok=ok)


class UpdateAsset(graphene.Mutation):
    class Arguments:
        pk = graphene.Int()
        product_id = graphene.Int()
        modded_product_name = graphene.String()
        cost = graphene.Int()
        existence = graphene.Int()
        properties = GenericScalar()
        tags_to_add = graphene.List(graphene.Int)
        tags_to_remove = graphene.List(graphene.Int)
        asset_type = graphene.String()
        category = graphene.String()
        duration = graphene.String()
        expires_at = graphene.String()
        starts_at = DateTime()
        is_deleted = graphene.Boolean()
        is_expired = graphene.Boolean()

    asset_id = graphene.Int()
    ok = graphene.Boolean()
    added_tags = graphene.List(graphene.Int)
    removed_tags = graphene.List(graphene.Int)
    failed_tags = graphene.List(graphene.Int)

    def mutate(self, info, **args):

        ok = False
        tags_to_add = args.pop("tags_to_add", [])
        tags_to_remove = args.pop("tags_to_remove", [])
        parsed_args = args.copy()
        if "starts_at" not in args:
            parsed_args["starts_at"] = timezone.now()
        if "expires_at" in args:
            parsed_args["duration"] = args["expires_at"] - parsed_args["starts_at"]
        elif "duration" in args:
            t = datetime.strptime(args["duration"], "%d days, %H:%M:%S")
            parsed_args["duration"] = timedelta(
                days=t.day, hours=t.hour, minutes=t.minute, seconds=t.second)
            parsed_args["expires_at"] = parsed_args["starts_at"] + parsed_args["duration"]

        parsed_args.update(
            cost=Money(args.get("cost", 0)))

        try:
            if args.get("pk") or args.get("modded_product_name"):
                if "pk" in args:
                    pk = parsed_args.pop("pk")
                    Asset.objects.filter(id=pk).update(**parsed_args)
                    asset = Asset.objects.filter(id=pk).first()
                elif args['modded_product_name']:
                    modded_product_name = parsed_args.pop('modded_product_name')
                    Asset.objects.filter(
                        modded_product_name=modded_product_name).update(
                            **parsed_args)
                    asset = Asset.objects.filter(
                        modded_product_name=modded_product_name).first()
                ok = True
        except:
            asset = None

        added_tags = []
        removed_tags = []
        failed_tags = []

        for tag_id in tags_to_add:
            try:
                tag = AssetTag.objects.get(pk=tag_id)
                asset.assettag_set.add(tag)
                added_tags.append(tag_id)
            except:
                failed_tags.append(tag_id)
                ok = False

        for tag_id in tags_to_remove:
            try:
                asset.assettag_set.remove(
                    AssetTag.objects.get(pk=tag_id))
                removed_tags.append(tag_id)
            except:
                failed_tags.append(tag_id)
                ok = False

        return UpdateAsset(
            asset_id=asset and asset.id or 0,
            added_tags=added_tags,
            removed_tags=removed_tags,
            failed_tags=failed_tags,
            ok=ok)
