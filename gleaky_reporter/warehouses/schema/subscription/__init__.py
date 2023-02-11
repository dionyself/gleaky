from graphene import ObjectType
from .invoice import InvoiceSubscription


class Subscription(ObjectType):
    invoice_subscription = InvoiceSubscription.Field()
