from django.urls import path, re_path

from . import views

app_name = 'studyapp'
urlpatterns = [
    path('', views.all_rooms, name='all_rooms'),
    re_path(r'token$', views.token, name="token"),
    re_path(r'rooms/(?P<slug>[-\w]+)/$', views.room_detail, name="room_detail"),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:meeting_id>/vote/', views.vote, name='vote'),
    path('api-call/', views.api_call, name='api-call'),
    path('courses/', views.CoursesView, name='courses'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path('profile/', views.ProfileView, name='profile'),
    path('map/', views.MapView, name='map')
    path('browse-meetings/', views.MeetingView, name="browse-meetings"),
    path('create-meetings/', views.CreateMeeting, name="create-meetings")
]
