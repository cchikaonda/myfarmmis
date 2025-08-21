from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

def root_redirect(request):
    return redirect('login')

urlpatterns = [
    path('', root_redirect),
    path('admin/', admin.site.urls),
    path('', include('farmers.urls')),
    path('', include('accounts.urls')),
    path('ration/', include('rationapp.urls')),
]
