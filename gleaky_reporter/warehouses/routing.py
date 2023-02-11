from graphene_django_subscriptions import GraphqlAPIDemultiplexer
from channels.routing import route_class
from warehouses.schema.subscription.invoice import InvoiceSubscription


class CustomAppDemultiplexer(GraphqlAPIDemultiplexer):
    consumers = {
      'invoices': InvoiceSubscription.get_binding().consumer,
    }


app_routing = [
    route_class(CustomAppDemultiplexer)
]
