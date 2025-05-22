from django.contrib import admin
from django.urls import path, include
from app_citas.views import login_view, registro_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('citas/', include('app_citas.urls')),
]
