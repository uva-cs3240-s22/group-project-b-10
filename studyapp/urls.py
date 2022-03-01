from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:meeting_id>/', views.detail, name='detail'),
    path('<int:meeting_id>/results/', views.results, name='results'),
    path('<int:meeting_id>/vote/', views.vote, name='vote'),
]