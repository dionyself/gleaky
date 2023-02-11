import graphene
from warehouses.models import Invoice
from graphene.types.generic import GenericScalar
from warehouses.serializers import InvoiceSerializer


class CreateInvoice(graphene.Mutation):
    class Arguments:
        fiscal_id = graphene.String()
        header = GenericScalar()
        body = GenericScalar()
        footer = GenericScalar()
        is_reversed = graphene.Boolean()
        is_blocked = graphene.Boolean()
        is_processed = graphene.Boolean()

    invoice_id = graphene.Int()
    ok = graphene.Boolean()

    def mutate(self, info, **args):

        ok = False
        try:
            serializer = InvoiceSerializer(data=args)
            serializer.is_valid(raise_exception=True)
            invoice = serializer.save()
            ok = True
        except:
            invoice = None

        return CreateInvoice(
            invoice_id=invoice and invoice.id or 0,
            ok=ok)


class UpdateInvoice(graphene.Mutation):
    class Arguments:
        pk = graphene.Int()
        fiscal_id = graphene.String()
        header = GenericScalar()
        body = GenericScalar()
        footer = GenericScalar()
        is_reversed = graphene.Boolean()
        is_blocked = graphene.Boolean()
        is_processed = graphene.Boolean()

    invoice_id = graphene.Int()
    ok = graphene.Boolean()

    def mutate(self, info, **args):

        ok = False
        invoice = None

        try:
            if 'pk' in args:
                pk = args.pop("pk")
                invoice = Invoice.objects.filter(id=pk).first()
                serializer = InvoiceSerializer(invoice, data=args, partial=True)
                serializer.is_valid(raise_exception=True)
                invoice = serializer.save()
                ok = True
        except:
            invoice = None

        return UpdateInvoice(
            invoice_id=invoice and invoice.id or 0,
            ok=ok)
