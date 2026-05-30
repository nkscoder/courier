from django.urls import path

from .views import courier

urlpatterns = [
    path("", courier, name="courier_view"),
]
