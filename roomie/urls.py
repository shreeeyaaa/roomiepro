from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import add_roomie, show_profiles, show_roomies
# from .views import profile_viewer, move_forward, move_backward


urlpatterns = [
    path("add_roomie", add_roomie, name="add_roomie"),
    path("show_roomies", show_roomies, name="add_roomie"),
    path("show_profiles", show_profiles, name="show_profiles")
    # path('profile/', profile_viewer, name='profile_viewer'),
    # path('move-forward/', move_forward, name='move_forward'),
    # path('move-backward/', move_backward, name='move_backward'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
