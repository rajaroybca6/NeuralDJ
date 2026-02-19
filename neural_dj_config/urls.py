from django.contrib import admin
from django.urls import path
from django.conf import settings # Add this
from django.conf.urls.static import static # Add this
from web_app.views import home, trigger_mix

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('mix/', trigger_mix, name='trigger_mix'),
]

# This connects your MEDIA_ROOT settings to your website
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)