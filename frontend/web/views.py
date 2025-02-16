from django.shortcuts import render
from web.utils.data import get_contacts


# Create your views here.
async def index(request):
    context = {"contacts": [], "error": None}
    try:
        contacts = await get_contacts()
        context["contacts"] = contacts
    except Exception as e:
        context["error"] = str(e)
    return render(request, "index.html", context)


def create_contact(request):
    return render(request, "create_content.html")
