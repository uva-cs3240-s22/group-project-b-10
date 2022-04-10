from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# I got this from a search tutorial 
# https://learndjango.com/tutorials/django-search-tutorial
from django.db.models import Q

from .models import Meeting, Reply, Course
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

    i = 0
    previous_course_title = ""
    for c in class_list:
        i+=1
        if(i>=2000):
            break

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

