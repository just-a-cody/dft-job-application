"""Views for the frontend"""

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django_htmx.http import retarget

import requests

from web.utils.data import (
    get_contacts,
    create_contact,
    delete_contact,
    get_contact_by_id,
    update_contact,
)
from web.utils.form import ContactForm


class IndexView(View):
    """Index view for the frontend"""

    base_template = "index.html"
    context = {"contacts": [], "error": None, "message": None}

    def get(self, request):
        """Get request for the index view"""

        self.context["message"] = None  # make sure message on every fetch is cleared
        self.get_contacts_from_api()
        self.get_message_params()
        return render(request, self.base_template, self.context)

    def delete(self, request):
        """Delete request for the index view"""

        contact_id = self.request.GET.get("contact_id")
        if contact_id is not None:
            try:
                delete_contact(contact_id)
                self.context["message"] = "successfully deleted a contact"
            except requests.exceptions.RequestException as e:
                self.context["message"] = f"failed to delete contact: {str(e)}"

        self.get_contacts_from_api()
        return render(request, self.base_template, self.context)

    def get_contacts_from_api(self):
        """Helper method to get contacts from the API"""

        try:
            contacts = get_contacts()
            self.context["contacts"] = contacts
        except requests.exceptions.RequestException as e:
            self.context["error"] = (
                f"Failed to fetch contacts list from backend: {str(e)}"
            )

    def get_message_params(self):
        """Helper method to get message params from the request"""

        message = self.request.GET.get("message", None)
        if message is not None:
            match message:
                case "contact-created-success":
                    self.context["message"] = "successfully created new contact"
                case "contact-created-failed":
                    self.context["message"] = "failed to create new contact"


class CreateContactView(View):
    """Create contact view for the frontend"""

    base_template = "create_contact.html"
    context = {}

    def get(self, request):
        """Get request for the create contact view"""

        form = ContactForm()  # make sure every GET request will have a new form
        self.context["form"] = form
        return render(request, self.base_template, self.context)

    def post(self, request):
        """Post request for the create contact view"""

        form = ContactForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            try:
                create_contact(form.cleaned_data)
                return redirect(
                    f"{reverse('web:index')}?message=contact-created-success"
                )
            except requests.exceptions.RequestException as e:
                self.context["message"] = (
                    f"failed to create new contact: {str(e)}. Please try again."
                )

        self.context["form"] = form
        response = render(
            request, "partials/create_contact_form.html", self.context
        )  # partial rendering
        return retarget(response, "#create_contact_form")


class EditContactView(View):
    """Edit contact view for the frontend"""

    base_template = "edit_contact.html"
    context = {}

    def get(self, request, contact_id):
        """Get request for the edit contact view"""

        data = get_contact_by_id(contact_id)

        if data is None:
            return redirect(f"{reverse('web:index')}?message=contact-not-found")

        form = ContactForm(data=data)
        self.context["form"] = form
        self.context["contact"] = data
        return render(request, self.base_template, self.context)

    def post(self, request, contact_id):
        """Post request for the edit contact view"""

        form = ContactForm(request.POST)
        if form.is_valid():
            update_contact(contact_id, form.cleaned_data)
            return redirect(f"{reverse('web:index')}?message=contact-updated-success")

        self.context["form"] = form
        response = render(
            request, "partials/edit_contact_form.html", self.context
        )  # partial rendering
        return retarget(response, "#edit_contact_form")
