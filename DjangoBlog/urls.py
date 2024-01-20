"""
URL configuration for DjangoBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.views.decorators.cache import never_cache
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('blogs/', include('blog.urls')),
]


if settings.DRF_ENABLED:

    schema_view = get_schema_view(
        openapi.Info(
            title="django blog API",
            default_version='v1',
            description="django blog API",
        ),
        permission_classes=(permissions.AllowAny,),
        patterns=urlpatterns,
    )
    # noinspection PyUnresolvedReferences
    schema = schema_view.with_ui('swagger')

    urlpatterns += [
        path('swagger/', never_cache(schema))
    ]
