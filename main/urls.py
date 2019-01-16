from .views import HomeView
from django.conf import settings
from django.conf.urls import url,static
from main import views


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^api/crawl/', views.crawl, name='crawl'),
]

# This is required for static files while in development mode. (DEBUG=TRUE)
# No, not relevant to scrapy or crawling :)
# if settings.DEBUG:
#     urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)