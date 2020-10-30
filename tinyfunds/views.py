from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Event
from .users.models import User
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import render
# from .forms import CommentsForm

class HomeView(generic.ListView):
    template_name = 'tinyfunds/index.html'
    content_object_name = 'user_list' 

    def get_queryset(self):
        return User.objects.all()

class ExploreView(generic.ListView):
    template_name = 'tinyfunds/explore.html'
    content_object_name = 'event_list' 

    def get_queryset(self):
        return Event.objects.all()

class EventView(generic.DetailView):
    template_name = 'account/event.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Event.objects

def event(request, pk):
    event = get_object_or_404(Event, idnum=pk)
    if (request.method == "POST"):
        new_title = request.POST['title'].strip()
        new_org_name = request.POST['org_name'].strip()
        new_event_pic = request.POST['event_pic'].strip()
        new_description = request.POST['description'].strip()
        new_event_date = request.POST['event_date'].strip()
        if new_title != "":
            event.title = new_title
        if new_description != "":
            event.description = new_description
        if new_org_name != "":
            event.org_name = new_org_name
        if new_event_pic != "":
            event.event_pic = new_event_pic
        event.save()
    return render(request, 'tinyfunds/explore.html', {
        'event': event,
    })