from django.urls import path, re_path

from . import views

app_name = 'studyapp'
urlpatterns = [
    path('', views.all_rooms, name='all_rooms'),
    path("favicon.ico", views.favicon),
    re_path(r'token$', views.token, name="token"),
    re_path(r'rooms/(?P<slug>[-\w]+)/$', views.room_detail, name="room_detail"),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:meeting_id>/vote/', views.vote, name='vote'),
    path('api-call/', views.api_call, name='api-call'),
    path('courses/', views.CoursesView, name='courses'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path('profile/', views.ProfileView, name='profile'),
    path('profile/<int:userID>/', views.OtherProfileView, name='view-other-profile'),
    path('map/', views.MapView, name='map'),
    path('browse-meetings/', views.MeetingView, name="browse-meetings"),
    path('create-meetings/', views.CreateMeeting, name="create-meetings"),
    path('enroll/', views.enroll_user_in_course, name = "enroll"),
    path('drop/', views.drop_course, name = "drop"),
    path('join/', views.join_meeting, name="join"),
    path('leave/', views.leave_meeting, name="leave"),
    path('meeting-successful/', views.meeting_successful_view, name="meeting-successful"),
    path('relevant-meetings/', views.RelevantMeetingsView, name="relevant-meetings"),
    path('send_friend_request/<int:userID>/', views.send_friend_request, name='send-friend-request'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept-friend-request'),
    path('browse-users/', views.FriendView, name="browse-users"),
    path('friend-requests/', views.RequestView, name="friend-requests")
]
