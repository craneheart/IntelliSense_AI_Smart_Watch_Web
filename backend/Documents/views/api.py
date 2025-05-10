from django.urls import path

from .docs import DocsView as Docs

urlpatterns = [
    path('docs/', Docs.as_view())
]
