from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include
from core import views
from core.apiv1 import apiv1

urlpatterns = [
    #path('courses/', views.course_list, name='course_list'),
    path('courses/', views.allCourse, name='all_courses'),
    path('courses-member-stats/', views.courseMemberStat, name='course_member_stats'),
    path('courses-stats/', views.courseStat, name='course_stats'),
    path('courses/<int:course_id>/', views.courseDetail, name='course_detail'),
    path('silk/', include('silk.urls', namespace='silk')), 
    path('api/v1/', apiv1.urls),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


