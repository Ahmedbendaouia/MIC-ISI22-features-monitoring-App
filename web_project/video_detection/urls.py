from django.urls import path,include,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('Flotation_froth/',views.Flotation_froth_display_page),
    path('Bubble_monitoring/', views.Bubble_size_monitoring_page),
    path('flotation_froth_frame',views.flotation_froth_frame,name="flotation_froth_frame"),    
    path('Otsu_frame',views.Otsu_frame,name="Otsu_frame"),
    path('spare_frame',views.spare_frame,name="spare_frame"),   
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]



