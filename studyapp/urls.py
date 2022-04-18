from django.urls import path

from . import views

app_name = 'studyapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:meeting_id>/vote/', views.vote, name='vote'),
    path('api-call/', views.api_call, name='api-call'),
    path('courses/', views.CoursesView, name='courses'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path('profile/', views.ProfileView, name='profile'),
    path('browse-meetings/', views.MeetingView, name="browse-meetings"),
    path('create-meetings/', views.CreateMeeting, name="create-meetings")
]
