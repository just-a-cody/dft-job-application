from django.shortcuts import render, redirect
from web.utils.data import get_contacts
from web.utils.form import ContactForm
from django_htmx.http import retarget
from django.urls import reverse
from django.views import View


class IndexView(View):
    base_template = "index.html"
    context = {"contacts": [], "error": None, "message": None}

    async def get(self, request):
        self.context["message"] = None  # make sure message on every fetch is cleared
        contacts = await self.get_contacts_from_api()
        self.get_message_params()
        self.context["contacts"] = contacts
        return render(request, self.base_template, self.context)

    """
    ------------ Helper methods --------------    
    """

    async def get_contacts_from_api(self):
        try:
            contacts = await get_contacts()
            self.context["contacts"] = contacts
        except Exception as e:
            self.context["error"] = f"Failed to fetch contacts list from backend: {str(e)}"

    def get_message_params(self):
        message = self.request.GET.get("message", None)
        if message is not None:
            match message:
                case "contact-created-success":
                    self.context["message"] = "successfully created new contact"


class CreateContactView(View):
    base_template = "create_contact.html"
    context = {}

    def get(self, request):
        form = ContactForm()  # make sure every GET request will have a new form
        self.context["form"] = form
        return render(request, self.base_template, self.context)

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            return redirect(f"{reverse('web:index')}?message=contact-created-success")
        else:
            self.context["form"] = form
            response = render(request, "partials/create_contact_form.html", self.context)  # partial rendering
            return retarget(response, "#create_contact_form")
