from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('forum/', include('forum.urls')),
    
    # This line should already be there
    path('', include('users.urls')), 
]