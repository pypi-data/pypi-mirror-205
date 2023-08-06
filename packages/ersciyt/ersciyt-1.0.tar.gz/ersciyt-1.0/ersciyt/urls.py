from django.urls import path
from . import views

urlpatterns = [
    path('', views.helping ),
    path('ytlink/', views.ytlink ),
    path('link/', views.ytlink ),
    path('yt/', views.ytlink ),
    path('youtube/', views.ytlink ),
    path('mp3/<str:link>/', views.ytmp3 ),
    path('ab/<str:time>/<str:link>/', views.abcut ),
    path('<str:lang>/<str:link>/', views.sub ),
    path('<str:link>/', views.ytdwn ),
]