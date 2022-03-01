from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    latest_reply_list = Meeting.objects.order_by('-post_date')[:5]
    output = ', '.join([m.post_text for m in latest_reply_list])
    return HttpResponse(output)

def detail(request, meeting_id):
    return HttpResponse("You're looking at meeting proposals %s." % meeting_id)

def results(request, meeting_id):
    response = "You're looking at the responses %s."
    return HttpResponse(response % meeting_id)

def vote(request, meeting_id):
    return HttpResponse("You're responding to the proposal %s." % meeting_id)