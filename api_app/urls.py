from django.urls import path
from api_app import views

urlpatterns = [
    path('future/', views.futureInsertView,  name='future-media'),
    path('popular/', views.isertPopularMovieView,  name='popular-media'),
    path('genres/', views.setGenres,  name='genres-media'),
    path('medias/', views.setMedias,  name='media'),
    path('v1/medias/', views.ListMedias.as_view(),  name='medias'),
    path('v1/medias/insert/', views.CreatMedia.as_view(),  name='medias_insert'),
    path('v1/lancaments/', views.ListLancaments.as_view(),  name='lancaments'),
    path('v1/lancaments/insert/', views.CreatLancaments.as_view(),  name='lancaments_insert'),
    path('v1/trends/', views.ListPopular.as_view(),  name='trends'),
    path('v1/trends/insert/', views.CreatPopular.as_view(),  name='trends_insert'),
    path('v1/trends/delete/<int:pk>', views.DeletePopularViews.as_view(),  name='trends_delete'),
    path('offset/<str:key>/', views.ImportOffsetView.as_view(), name='import-offset'),
]
