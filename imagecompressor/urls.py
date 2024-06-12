from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from image_processing.views import home

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('image-processing/', include("image_processing.urls")),
    path('auth/', include("authentication.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
