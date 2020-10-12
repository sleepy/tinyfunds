from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Event
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import render
# from .forms import CommentsForm

class HomeView(generic.ListView):
    template_name = 'tinyfunds/index.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Event.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class AccountView(generic.DetailView):
    template_name = 'account/account.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())