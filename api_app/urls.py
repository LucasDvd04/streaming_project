from django.urls import path
from api_app import views

urlpatterns = [
    path('future/', views.futureInsertView,  name='future-media'),
    path('popular/', views.isertPopularMovieView,  name='popular-media'),
    path('genres/', views.setGenres,  name='genres-media'),
    path('medias/', views.setMedias,  name='media'),
]
