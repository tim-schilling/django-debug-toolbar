from django.http import JsonResponse
from django.shortcuts import render


def increment(request):
    try:
        value = int(request.session.get("value", 0)) + 1
    except ValueError:
        value = 1
    request.session["value"] = value
    return JsonResponse({"value": value})


def jinja_session_view(request):
    if not request.session.get("jinja_session_view"):
        request.session["jinja_session_view"] = True
    return render(request, "jinja2/session.jinja")
