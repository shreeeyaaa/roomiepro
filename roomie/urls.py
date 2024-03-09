from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import add_roomie, show_profiles, show_roomies

urlpatterns = [
    path("add_roomie", add_roomie, name="add_roomie"),
    path("show_roomies", show_roomies, name="add_roomie"),
    path("show_profiles", show_profiles, name="show_profiles")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
