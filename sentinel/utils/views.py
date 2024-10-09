import json

from django.http import HttpResponse
from sentinel.utils.models import City


def GetCityProvince(request):

    if request.is_ajax():
        q = request.GET.get('term', '')

        cities = City.objects.filter(province=q).order_by('name')
        results = []
        for city in cities:
            city_json = {}
            city_json['id'] = city.id
            city_json['name'] = city.name
            results.append(city_json)

        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
