from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# I got this from a search tutorial 
# https://learndjango.com/tutorials/django-search-tutorial
from django.db.models import Q
from .models import Profile

# see https://www.twilio.com/blog/2018/05/build-chat-python-django-applications-programmable-chat.html
from django.conf import settings
from django.http import JsonResponse
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

from .models import Meeting, Reply, Course, Profile, Room
from .forms import MeetingCreateForm
from .models import Meeting, Reply, Course, Profile, Friend_Request
import requests


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'studyapp/index.html'
    context_object_name = 'latest_reply_list'

    def get_queryset(self):
        return Meeting.objects.filter(post_date__lte=timezone.now()).order_by('-post_date')[:5]

class DetailView(generic.DetailView):
    model = Meeting
    template_name = 'studyapp/detail.html'

    def get_queryset(self):
	    return Meeting.objects.filter(post_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Meeting
    template_name = 'studyapp/results.html'

class SearchResultsView(generic.ListView):
    model = Course
    template_name = "studyapp/search_results.html"

    def get_queryset(self):  
        query = self.request.GET.get("q")
        object_list = Course.objects.filter(
            Q(course_name__icontains=query) | Q(department__icontains=query)
        )
        return object_list

def vote(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    try:
        selected_reply = meeting.reply_set.get(pk=request.POST['choice'])
    except (KeyError, Reply.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'studyapp/detail.html', {
            'meeting': meeting,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_reply.votes += 1
        selected_reply.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('studyapp:results', args=(post.id,)))

def get_data():
	url = 'https://api.devhub.virginia.edu/v1/courses'
	data = requests.get(url).json()
	return data

def CoursesView(request):
    model = Course
    template_name = 'studyapp/courses.html'
    courses_list = Course.objects.order_by('course_name')
    context = {'courses_list': courses_list}
    return render(request, template_name, context)

def ProfileView(request):
    model = Profile
    template_name = 'studyapp/profile.html'
    myProfile = Profile.objects.get(user = request.user)
    context = {'profile': myProfile}
    return render(request, template_name, context)

# https://www.fullstackpython.com/blog/maps-django-web-applications-projects-mapbox.html
def MapView(request):
    template_name = 'studyapp/map.html'
    # myProfile = Profile.objects.get(user = request.user)
    # context = {'profile': myProfile}
    # return render(request, template_name)
    # TODO: move this token to Django settings from an environment variable
    # found in the Mapbox account settings and getting started instructions
    # see https://www.mapbox.com/account/ under the "Access tokens" section
    mapbox_access_token = 'pk.my_mapbox_access_token';#'pk.eyJ1Ijoicm9ucmFuMTIzIiwiYSI6ImNsMjJwOTJ3bjFpbGYzaXFkc242eW9ncHAifQ.Y6LOXAW4nJqm7SCOeH_Qgg';
    return render(request, template_name,
                  {'mapbox_access_token': mapbox_access_token })
# idea here is we let users browse all the upcoming meetings, so they can add the ones they want
def MeetingView(request):
    model = Meeting
    template_name = 'studyapp/browse-meetings.html'
    all_meetings = Meeting.objects.order_by('post_date')
    context = {'all_meetings': all_meetings}
    return render(request, template_name, context)

def CreateMeeting(request):
    # model = Thought
    template_name = 'studyapp/create-meetings.html'
    form = MeetingCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        
    context = {
        'form': form 
        }
    return render(request, template_name, context)

def api_call(request):
    # find a way to clear the database or update before repopulating
    try:
        courses = Course.objects.all()
        courses.delete()
        print()
    except:
        print('There are no courses!', courses.count())

    # Load in a bunch of course class objects with api
        # make sure there are no repeating classes
    class_list = get_data()['class_schedules']['records']

    # i = 0
    previous_course_title = ""
    for c in class_list:
        # I'm commenting this part out because I think we want to load every class 
        # i+=1
        # if(i>=2000):
        #     break

        # print(c)
        if c[-1] == "2022 Spring":
            course_info = str(c[0]) + ' ' + str(c[1]) + '-' + str(c[2])
            department_code = str(c[0])
            course_title = str(c[4])
            if (previous_course_title != course_title):
            # print(course_info)
                previous_course_title = course_title
                Course.objects.create(course_name=course_title, department = department_code)

    # maybe display something on page when updated --> optional
    return render(request, 'studyapp/api-call.html')

# Twilio code for rooms
def all_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'studyapp/index.html', {'rooms': rooms})


def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'studyapp/room_detail.html', {'room': room})


fake = Faker()

def token(request):
    identity = request.GET.get('identity', Profile.objects.get(user = request.user).name)
    device_id = request.GET.get('device', 'default')  # unique device ID

    # print("token views")

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'token': token.to_jwt()
    }

    return JsonResponse(response)

def send_friend_request(request, userID):
    from_user = Profile.objects.get(user=request.user)
    to_user = Profile.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return HttpResponse('Friend request sent!')
    else:
        return HttpResponse('Friend request already pending')

def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('Friend request accepted!')
    else:
        return HttpResponse('Friend request denied')