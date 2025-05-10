from django.urls import path, include, re_path

from vue.vue import Index
from .views import api

urlpatterns = [
    re_path(r'^(?!api/).*$', Index.get("Documents")),
    path("api/", include(api)),
]
