from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
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
from .models import Meeting, Reply, Course, Profile
import requests

from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

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
            Q(course_title__icontains=query) | Q(course_name__icontains=query) | Q(department__icontains=query) | Q(course_number__icontains=query)
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



def RelevantMeetingsView(request):
    myProfile = Profile.objects.get(user = request.user)
    my_courses = myProfile.profile_courses.all()
    # print(my_courses)
    all_meetings = Meeting.objects.all()
    relevant_meetings = []
    for meeting in all_meetings:
        if meeting.course in my_courses:
            relevant_meetings.append(meeting)

    template_name = 'studyapp/browse-meetings.html'
    context = {'all_meetings': relevant_meetings}
    return render(request, template_name, context)
    


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
    template_name = 'studyapp/create-meetings.html'
    form = MeetingCreateForm(request.POST or None)
    if form.is_valid():
        new_meeting = form.save()
        # print(f.id)
        # append the meeting to user profile
        myProfile = Profile.objects.get(user = request.user)
        # meeting_id = request.POST['meeting_id']
        meeting_id = new_meeting.id
        meeting = Meeting.objects.get(id = meeting_id)
         # this part appends the meeting to the user
        myProfile.meetings.add(meeting)
        
        meeting = Meeting.objects.get(id = meeting_id)

        myProfile.meetings.add(meeting)
        myProfile.save()

        meeting.buddies.add(myProfile)
        meeting.save()
        return HttpResponseRedirect("/meeting-successful/")
    context = {
        'form': form 
        }
        

    return render(request, template_name, context)

def meeting_successful_view(request):
    template_name = 'studyapp/meeting-successful.html'
    return render(request, template_name)

# added course as a parameter so hopefully it enrolls that course?
def enroll_user_in_course(request):
    
    if request.method != 'POST':
        return  HttpResponse('Method Not Allowed', status=405)
    # where we take them back to
    next_url = request.POST['next']
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    # Now assuming user is authenticated correctly
    # get the current user 
    myProfile = Profile.objects.get(user = request.user)
    course_id = request.POST['course_id']
    course = Course.objects.get(id = course_id)
    myProfile.profile_courses.add(course)
    myProfile.save()

    return redirect(next_url)

def drop_course(request):
    if request.method != 'POST':
        return  HttpResponse('Method Not Allowed', status=405)
    # where we take them back to
    next_url = request.POST['next']
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    # Now assuming user is authenticated correctly
    # get the current user 
    myProfile = Profile.objects.get(user = request.user)
    course_id = request.POST['course_id']
    course = Course.objects.get(id = course_id)
    myProfile.profile_courses.remove(course)
    myProfile.save()
    return redirect(next_url)

def join_meeting(request):
    if request.method != 'POST':
        return  HttpResponse('Method Not Allowed', status=405)
    # where we take them back to
    next_url = request.POST['next']
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    # Now assuming user is authenticated correctly
    # get the current user 
    myProfile = Profile.objects.get(user = request.user)
    meeting_id = request.POST['meeting_id']
    meeting = Meeting.objects.get(id = meeting_id)
    # this part appends the meeting to the user
    myProfile.meetings.add(meeting)
    myProfile.save()
    # now we need to append the user to the meeting
    meeting.buddies.add(myProfile)
    meeting.save()
    return redirect(next_url)

def leave_meeting(request):
    if request.method != 'POST':
        return  HttpResponse('Method Not Allowed', status=405)
    # where we take them back to
    next_url = request.POST['next']
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    # Now assuming user is authenticated correctly
    # get the current user 
    myProfile = Profile.objects.get(user = request.user)
    meeting_id = request.POST['meeting_id']
    meeting = Meeting.objects.get(id = meeting_id)
    # this part appends the meeting to the user
    myProfile.meetings.remove(meeting)
    myProfile.save()
    # now we need to append the user to the meeting
    meeting.buddies.remove(myProfile)
    meeting.save()
    return redirect(next_url)

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
        if c[-1] == "2022 Fall":
            course_title = str(c[0]) + ' ' + str(c[1])
            department_code = str(c[0]) # Subject
            course_number = str(c[1]) # catalog_number
            course_name = str(c[4]) # Class Title
            if (previous_course_title != course_title):
            # print(course_info)
                previous_course_title = course_title
                Course.objects.create(course_name=course_name, course_number= course_number,department = department_code, course_title=course_title)

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
    # print(device_id)
    # print("token views")

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)
    
    # print(token)
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

@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "studyapp" / "static" / "favicon.png").open("rb")
    return FileResponse(file)