from graphene_django_subscriptions import Subscription
from warehouses.serializers import InvoiceSerializer


class InvoiceSubscription(Subscription):

    @classmethod
    def subscription_resolver(cls, root, info, **kwargs):
        result = super().subscription_resolver(root, info, **kwargs)
        #from rx import Observable
        #result = Observable.from_iterable([result])
        return result

    class Meta:
        queryset = None
        serializer_class = InvoiceSerializer
        stream = 'invoices'
        description = 'Invoice Subscription'
