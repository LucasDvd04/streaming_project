from django.urls import path
from atlas_app import views

urlpatterns = [
    path('', views.homeView,  name='home'),
    path('detail/<int:pk>/', views.MediaDetailView.as_view(),  name='detail_media'),
    path('movies/', views.MoviesListView.as_view(),  name='movies_media'),
    path('series/', views.SeriesListView.as_view(),  name='series_media'),
]
