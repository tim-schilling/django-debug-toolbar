from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from rest_framework import viewsets, serializers

from rest_framework.routers import DefaultRouter

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="index.html")),
    url(r"^jquery/$", TemplateView.as_view(template_name="jquery/index.html")),
    url(r"^mootools/$", TemplateView.as_view(template_name="mootools/index.html")),
    url(r"^prototype/$", TemplateView.as_view(template_name="prototype/index.html")),
    url(r"^admin/", admin.site.urls),
] + router.urls

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [url(r"^__debug__/", include(debug_toolbar.urls))]
