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
    #def get_queryset(self):
    #    return Event.objects.filter(
    #        pub_date__lte=timezone.now()
    #    ).order_by('-pub_date')[:5]

