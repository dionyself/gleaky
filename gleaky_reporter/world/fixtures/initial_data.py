from dynamic_initial_data.base import BaseInitialData
from world.models import Country
from django_countries import countries, Country as CountrySource


class InitialData(BaseInitialData):
    dependencies = ['my_first_app', 'my.second.app']

    def update_initial_data(self):
        for code, name in list(countries):
            country = CountrySource(code,)
            upt_ins = {
                "name": country.name,
                "code": country.code,
                "flag": country.flag,
                "numeric": country.numeric(code),
                "numeric_padded": country.numeric(code, padded=True),
                "alpha3": country.alpha3(code),
            }
        model_obj, created = TestModel.objects.upsert(int_field=5, defaults={'float_field': 2.0})

        TestModel.objects.bulk_upsert([
            TestModel(float_field=1.0, char_field='1', int_field=1),
            TestModel(float_field=2.0, char_field='2', int_field=2),
            TestModel(float_field=3.0, char_field='3', int_field=3),
        ], ['int_field'], ['char_field'])
