from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('atlas_app.urls'), name="atlas"),
    path('api/', include('api_app.urls'), name="api"),
    path('', include('accounts.urls'), name="accounts"),

]
