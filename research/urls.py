from django.contrib import admin
from django.urls import path, include
from main.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='main'),
    path('', include('authenticate.urls')),
    path('', include('main.urls')),
]