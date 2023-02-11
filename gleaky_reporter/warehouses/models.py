from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.postgres.fields import JSONField
from world.models import Product, Country, Corporation, TenantUser, Review, ReviewComment, BaseModel


class Region(BaseModel):
    country = models.ForeignKey(Corporation, null=True, blank=True)
    region_type = models.CharField(max_length=24) # state | province
    is_capital = models.BooleanField(default=False)

class City(BaseModel):
    region = models.ForeignKey(Region, null=True, blank=True)
    is_capital = models.BooleanField(default=False)

class Store(BaseModel):
    created_on = models.DateField(auto_now_add=True)
    corporation = models.ForeignKey(Corporation, null=True, blank=True)
    phone = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    time_zone = models.CharField(max_length=100, null=True, blank=True)

class Asset(BaseModel):
    product = models.ForeignKey(Product, null=True, blank=True)
    modded_product_name = models.TextField(null=True, blank=True, unique=True)
    cost = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    minimal_earnings = models.IntegerField(default=0)
    availability = models.IntegerField(default=0)
    existence = models.IntegerField(default=0)
    asset_type = models.TextField(default="product")
    category = models.TextField(null=True, blank=True)
    starts_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

class AssetTag(BaseModel):
    tag_type = models.TextField(null=True, blank=True)
    priority = models.IntegerField(default=0)
    properties = JSONField(null=True, blank=True)
    assets = models.ManyToManyField(Asset)

class Invoice(BaseModel):
    fiscal_id = models.TextField()
    header = JSONField(null=True, blank=True)
    body = JSONField(null=True, blank=True)
    footer = JSONField(null=True, blank=True)
    is_reversed = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
