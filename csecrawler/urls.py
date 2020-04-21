from django.contrib import admin
from django.urls import path
from cse_notice import views as notices

urlpatterns = [
    path('admin/', admin.site.urls),
	path('notice/', notices.index),
]
