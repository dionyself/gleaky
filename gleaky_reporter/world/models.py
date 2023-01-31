from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django_countries import ioc_data
from django_countries.conf import settings


class Country(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    flag = models.CharField(max_length=512)
    flag_css = models.CharField(max_length=512)
    unicode_flag = models.CharField(max_length=512)
    code = models.CharField(max_length=2)
    alpha3 = models.CharField(max_length=3)
    numeric = models.IntegerField()
    on_trial = models.BooleanField()
    numeric_padded = models.CharField(max_length=3)
    created_on = models.DateField(auto_now_add=True)
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
        """
        Output the css classes needed to display an HTML element as a flag
        sprite.
        Requires the use of 'flags/sprite.css' or 'flags/sprite-hq.css'.
        Usage example::
            <i class="{{ ctry.flag_css }}" aria-label="{{ ctry.code }}></i>
        """
        if not self.code:
            return ""
        return "flag-sprite flag-{} flag-_{}".format(*self.code.lower())

    @property
    def unicode_flag(self):
        """
        Generate a unicode flag for the given country.
        The logic for how these are determined can be found at:
        https://en.wikipedia.org/wiki/Regional_Indicator_Symbol
        Currently, these glyphs appear to only be supported on OS X and iOS.
        """
        if not self.code:
            return ""

        # Don't really like magic numbers, but this is the code point for [A]
        # (Regional Indicator A), minus the code point for ASCII A. By adding
        # this to the uppercase characters making up the ISO 3166-1 alpha-2
        # codes we can get the flag.
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
