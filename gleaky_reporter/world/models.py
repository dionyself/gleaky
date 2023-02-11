from django.db import models
from django.contrib.postgres.fields import JSONField
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase
from django_countries import ioc_data
from django_countries.conf import settings
from tenant_users.tenants.models import UserProfile


class BaseModel(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(max_length=200)
    properties = JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)


class TenantUser(UserProfile):
    name = models.CharField(
        max_length = 100,
        blank = True,
    )

class Country(TenantBase):
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(max_length=200)
    paid_until = models.DateField()
    description = models.TextField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    time_zone = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    flag = models.CharField(max_length=512)
    flag_css = models.CharField(max_length=512)
    unicode_flag = models.CharField(max_length=512)
    code = models.CharField(max_length=2)
    alpha3 = models.CharField(max_length=3)
    numeric = models.IntegerField()
    on_trial = models.BooleanField()
    numeric_padded = models.CharField(max_length=3)
    created_on = models.DateField(auto_now_add=True)
    properties = JSONField(null=True, blank=True)
    auto_create_schema = True

    @property
    def flag(self):
        if not self.code:
            return ""
        flag_url = self.flag_url
        if flag_url is None:
            flag_url = settings.COUNTRIES_FLAG_URL
        url = flag_url.format(code_upper=self.code, code=self.code.lower())
        if not url:
            return ""
        url = urlparse.urljoin(settings.STATIC_URL, url)
        return self.maybe_escape(url)

    @property
    def flag_css(self):
        if not self.code:
            return ""
        return "flag-sprite flag-{} flag-_{}".format(*self.code.lower())

    @property
    def unicode_flag(self):
        if not self.code:
            return ""
        OFFSET = 127397
        points = [ord(x) + OFFSET for x in self.code.upper()]
        return chr(points[0]) + chr(points[1])

    @staticmethod
    def country_from_ioc(ioc_code, flag_url=""):
        code = ioc_data.IOC_TO_ISO.get(ioc_code, "")
        if code == "":
            return None
        return Country.objects.get_or_none(code)

    @property
    def ioc_code(self):
        return ioc_data.ISO_TO_IOC.get(self.code, "")

class Domain(DomainMixin):
    pass

class GeopoliticalBorder(BaseModel):
    area_data = models.CharField(max_length=100)
    countries = models.ManyToManyField(Country, null=True, blank=True)

class GeopoliticalOrganization(BaseModel):
    countries = models.ManyToManyField(Country, null=True, blank=True)

class Product(BaseModel):
    code = models.IntegerField(null=True, blank=True)
    code_type = models.TextField()
    existence_type = models.TextField()

    class Meta:
        unique_together = ("code", "code_type")

class Conglomerate(BaseModel):
    country = models.ForeignKey(Country)
    related_corporation = models.ForeignKey("self", null=True)
    phone = models.CharField(max_length=100)

class Corporation(BaseModel):
    country = models.ForeignKey(Country)
    conglomerate = models.ForeignKey(Conglomerate, null=True, blank=True)
    related_corporation = models.ForeignKey("self", null=True)
    phone = models.CharField(max_length=100)

class Review(BaseModel):
    user = models.ForeignKey(TenantUser)
    product = models.ForeignKey(Product)
    title = models.TextField()
    content = models.TextField()
    comments = models.TextField()
    stars = models.IntegerField()
    likes = models.ManyToManyField(TenantUser, related_name="reviews_liked")
    dislikes = models.ManyToManyField(TenantUser, related_name="reviews_disliked")

class ReviewComment(BaseModel):
    user = models.ForeignKey(TenantUser)
    content = models.TextField(help_text="Comment content.")
    likes = models.ManyToManyField(TenantUser, related_name="review_comments_liked")
    dislikes = models.ManyToManyField(TenantUser, related_name="review_comments_disliked")