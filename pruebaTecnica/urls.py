from django.contrib import admin
from django.urls import path, include
from apps.core import urls as home
from apps.scraping import urls as scraping
from apps.exchange import urls as exchange

urlpatterns = [
    path('admin', admin.site.urls),
    path('', include(home)),
    path('scraping',include(scraping)),
    path('exchange',include(exchange)),
]
