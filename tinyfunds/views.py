from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Event
from .users.models import User
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView
from django.utils import timezone
from django.shortcuts import render
from .forms import CreateEventForm
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
    template_name = 'tinyfunds/event.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Event.objects

class CreateEventView(CreateView):

    template_name = 'tinyfunds/create_event.html'
    form_class = CreateEventForm 


    def get(self, request, *args, **kwargs):
        context = {'form': CreateEventForm()}
        return render(request, 'tinyfunds/create_event.html', context=context)
    
    def post(self, request, *args, **kwargs):
        form = CreateEventForm(request.POST)
        if form.is_valid():
            event = form.save()
            event.save()
            return HttpResponseRedirect(reverse('event', args=[event.id]))
        
        return render(request, 'tinyfunds/create_event.html', {
                'form':form,
            })




def event(request, pk):
    event = get_object_or_404(Event, id=pk)

    if (request.method == "POST"):
        new_title = request.POST['title'].strip()
        new_org_name = request.POST['org_name'].strip()
        new_pic = request.POST['pic'].strip()
        new_description = request.POST['info'].strip()
        new_event_date = request.POST['event_date'].strip()
        if new_title != "":
            event.title = new_title
        if new_description != "":
            event.description = new_description
        if new_org_name != "":
            event.org_name = new_org_name
        if new_pic != "":
            event.pic = new_pic
        event.save()
    return HttpResponseRedirect(reverse('event', args=[pk]))
