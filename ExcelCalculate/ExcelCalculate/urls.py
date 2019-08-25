from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('email/', include('sendEmail.urls'), name='email'),
    path('calculate/', include('calculate.urls'), name='calculate'),
    path('', include('main.urls'), name='main'),
    path('admin/', admin.site.urls),
]
