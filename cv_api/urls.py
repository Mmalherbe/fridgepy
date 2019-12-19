
from django.conf.urls import url, include
from face_detector.views import detect
from django.contrib import admin
from face_detector import views
admin.autodiscover()

urlpatterns = [
url(r'^detect/',views.detect , name='detect'),
    #url(r'^$',views.home , name='home'),
    # url(r'^$', 'cv_api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

   # url(r'^admin/', include(admin.site.urls)),
]