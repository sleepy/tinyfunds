from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import render

from .models import User

class AccountView(generic.DetailView):
    template_name = 'account/account.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return User.objects

def user(request, pk):
    user = get_object_or_404(User, id=pk)
    if (request.method == "POST"):
        new_name = request.POST['name'].strip()
        new_bio = request.POST['bio'].strip()
        new_pfp = request.POST['pfp'].strip()
        if new_name != "":
            user.name = new_name
        if new_bio != "":
            user.bio = new_bio
        if new_pfp != "":
            user.pfp = new_pfp
        user.save()
    return render(request, 'account/account.html', {
        'user': user,
        'privileged': False,
    })

def filter_by_donation_amt(request):
    if (request.method == "POST"):
        return User.objects.order_by('total_donated')

def filter_by_vol_hours(request):
    if (request.method == "POST"):
        return User.objects.order_by('total_hours_pledged')





