from django.db import models, transaction
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point


class ServiceArea(gis_models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    poly = gis_models.PolygonField()

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=14)
    # use choices
    language = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    areas = models.ManyToManyField(to=ServiceArea, related_name='areas')
    deleted = models.BooleanField(default=False)

    @classmethod
    def create(cls, values):
        obj = cls(name=values.get('name'),
                  email=values.get('email'),
                  phone_number=values.get('phone_number'),
                  language=values.get('language'),
                  currency=values.get('currency'))
        with transaction.atomic():
            obj.save()

            areas = []
            for i in values.get('areas'):
                areas.append(ServiceArea(name=i.get('name'),
                                         price=i.get('price'),
                                         poly=i.get('poly')))

            obj.areas.set(ServiceArea.objects.bulk_create(areas))
            obj.save()

        return obj

    @classmethod
    def lookup_point(cls, lat, lng):
        point = Point(float(lat), float(lng), srid=4326)
        service_areas = ServiceArea.objects.filter(poly__contains=point)
        return cls.objects.filter(areas__in=service_areas)

    def delete(self):
        self.delete = True
        self.save()

    def __str__(self):
        return self.name
