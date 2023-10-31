from django.urls import path, include
from . import views
from .views import bulk_upload_items

app_name = 'app'

urlpatterns = [
    path('', views.index, name="index"),
    path('bulk-upload/', bulk_upload_items, name='bulk-upload'),
]
