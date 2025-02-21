from django.urls import path
from . import views

app_name = "web"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create-contact", views.CreateContactView.as_view(), name="create_contact"),
    path(
        "edit/<uuid:contact_id>",
        views.EditContactView.as_view(),
        name="edit_contact",
    ),
]
