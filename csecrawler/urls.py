from django.contrib import admin
from django.urls import path
from cse_notice import views as notices
from login import views as login_page
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (handler400, handler403, handler404, handler500)

handler400 = 'cse_notice.views.bad_request'
handler403 = 'cse_notice.views.permission_denied'
handler404 = 'cse_notice.views.page_not_found'
handler500 = 'cse_notice.views.server_error'

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [    
    path('admin/', admin.site.urls, name='admin'),
    path('mainpage/', notices.mainpage, name='mainpage'),
	path('csenotices/', notices.csenotice, name='csenotices'),
	path('videos/', notices.video, name='videos'),
	path('reports/', notices.report, name='reports'),
	path('notices/', notices.notice, name='notices'),
	path('materials/', notices.material, name='materials'),
    path('login/', login_page.login, name='login'),
    path('logout/', login_page.logout, name='logout'),
    path('signup/', login_page.signup, name='signup'),
    path('setting/', login_page.setting, name='setting'),
]
