from django.urls import path
from .views import predictForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", predictForm, name="predict-form"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
