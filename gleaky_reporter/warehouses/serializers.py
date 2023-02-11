from rest_framework import serializers
from warehouses.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('id', 'fiscal_id', 'created_at')
