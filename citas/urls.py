
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url

#router = DefaultRouter()
#router.register(r'citas', views.CitasList)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('citas.urls')),
    
]

# urlpatterns = [
#     url(r'^citas$', views.Citas.as_view()),

# ]