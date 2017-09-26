from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/v1/animals/(?P<pk>[0-9]+)$',
        views.get_animal,
        name='get_animal'),
    url(r'^api/v1/animals$',
        views.get_animals,
        name='get_animals'),
    url(r'^api/v1/checked-out-animals$',
        views.get_checked_out_animals,
        name='get_checked_out_animals'),
]
