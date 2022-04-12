from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('map_example/', include('map_example.urls')),
    path('admin/', admin.site.urls),
    path("markers/", include("markers.urls")),
]