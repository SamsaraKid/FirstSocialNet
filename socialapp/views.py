from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User, Group
from django.views import generic
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def index(req):
    if req.user.username:
        username = req.user.username
        print('имя', req.user.profile.name)
    else:
        username = 'Guest'
    data = {'username': username, 'form': LogInForm()}
    return render(req, 'index.html', context=data)


def registration(req):
    if req.POST:
        userform = UserForm(req.POST)
        profileform = ProfileForm(req.POST)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            profile = Profile.objects.get(user=user)
            print(profileform.cleaned_data.get('name'))
            print(Profile.objects.get(user=user).user.username, Profile.objects.get(user=user).name)
            profile.name = profileform.cleaned_data.get('name')
            print(profile.name)
            print(Profile.objects.get(user=user).user.username, Profile.objects.get(user=user).name)
            profile.surname = profileform.cleaned_data.get('surname')
            profile.save()
            user.save()
            print(profile.name)
            print(Profile.objects.get(user=user).user.username, Profile.objects.get(user=user).name)
            login(req, user)
            print(profile.name)
            print(Profile.objects.get(user=user).user.username, Profile.objects.get(user=user).name)
            return HttpResponseRedirect(reverse('profile', args=[req.user.profile.slug]))
    else:
        userform = UserForm()
        profileform = ProfileForm()
    data = {'userform': userform, 'profileform': profileform}
    return render(req, 'registration/registration.html', context=data)


@login_required
def afterlogin(req):
    return HttpResponseRedirect(reverse('profile', args=[req.user.profile.slug]))


# def profile(req, user_slug):
#     profile = get_object_or_404(Profile, slug=user_slug)
#     return render(req, 'socialapp/profile_detail.html', context={'profile': profile})


class ProfileDetail(generic.DetailView):
    model = Profile
    slug_url_kwarg = 'slug'


