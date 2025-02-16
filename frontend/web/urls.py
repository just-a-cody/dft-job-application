from django.urls import path
from . import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path("create-contact", views.create_contact, name="create_contact"),
]
