from django.urls import path,include
from . import views

urlpatterns = [
    path('display/',views.home),
    path('flotation_froth_frame',views.flotation_froth_frame,name="flotation_froth_frame"),    
    path('Otsu_frame',views.Otsu_frame,name="Otsu_frame"),
    path('spare_frame',views.spare_frame,name="spare_frame"),
    path('stream', views.speed_stream, name='test_stream'),    
    path('home', views.test, name='home'),
    path('image', views.image_test, name='image')    
]


