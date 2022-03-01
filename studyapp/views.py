from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import Meeting

# Create your views here.

def index(request):
    latest_post_list = Meeting.objects.order_by('-post_date')[:5]
    template = loader.get_template('studyapp/index.html')
    context = {
        'latest_post_list': latest_post_list,
    }
    return render(request, 'studyapp/index.html', context)

def detail(request, meeting_id):
    post = get_object_or_404(Meeting, pk = meeting_id)
    return render(request, 'studyapp/detail.html', {'post': post})

def results(request, meeting_id):
    response = "You're looking at the responses %s."
    return HttpResponse(response % meeting_id)

def vote(request, meeting_id):
    return HttpResponse("You're responding to the proposal %s." % meeting_id)