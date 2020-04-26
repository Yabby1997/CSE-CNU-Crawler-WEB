from django.contrib import admin
from django.urls import path
from cse_notice import views as notices
from login import views as login_page

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('notice/', notices.index, name='notice'),
    path('login/', login_page.login, name='login'),
    path('signup/', login_page.signup, name='signup'),
]
