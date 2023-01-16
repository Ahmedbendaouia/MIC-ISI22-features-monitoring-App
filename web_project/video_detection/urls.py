from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('Flotation_froth/', views.Flotation_froth_display_page),
    path('Bubble_monitoring/', views.Bubble_size_monitoring_page),
    path('video_feed/',views.video_feed_page,name="video_feed_page"),
    path('video_feed/<int:pk>', views.toggle_in_charge, name='video_feed'),
    path('video_feed/delete/<int:pk>/', views.delete_video_feed, name='delete_feed'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
