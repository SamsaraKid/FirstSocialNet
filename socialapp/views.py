from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User, Group
from django.views import generic
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def index(req):
    if req.user.username:
        return HttpResponseRedirect(reverse('profile', args=[req.user.profile.slug]))
    if req.method == 'POST':
        form = AuthenticationForm(req, data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(req, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(req, 'index.html', {'form': form})
    # if req.user.username:
    #     return HttpResponseRedirect(reverse('profile', args=[req.user.profile.slug]))
    # else:
    #     username = 'Guest'
    # data = {'username': username, 'form': LogInForm()}
    # return render(req, 'index.html', context=data)


# def registration(req):
#     if req.POST:
#         userform = UserForm(req.POST)
#         profileform = ProfileForm(req.POST)
#         if userform.is_valid() and profileform.is_valid():
#             user = userform.save()
#             user.set_password(user.password)
#             user.save()
#             login(req, user)
#             profile = Profile.objects.get(user=user)
#             profile.name = profileform.cleaned_data.get('name')
#             profile.surname = profileform.cleaned_data.get('surname')
#             profile.save()
#             return HttpResponseRedirect(reverse('profile', args=[req.user.profile.slug]))
#     else:
#         userform = UserForm()
#         profileform = ProfileForm()
#     data = {'userform': userform, 'profileform': profileform}
#     return render(req, 'registration/registration.html', context=data)


def registration(req):
    if req.POST:
        userform = SignUp(req.POST, req.FILES)
        if userform.is_valid():
            user = userform.save()
            user.email = userform.cleaned_data.get('email')
            user.save()
            login(req, user)
            profile = Profile.objects.get(user=user)
            profile.name = userform.cleaned_data.get('name')
            profile.surname = userform.cleaned_data.get('surname')
            profile.secondname = userform.cleaned_data.get('secondname')
            profile.birthdate = userform.cleaned_data.get('birthdate')
            if userform.cleaned_data.get('city_custom'):
                new_city = City.objects.create(country=userform.cleaned_data.get('country'),
                                               name=userform.cleaned_data.get('city_custom'),
                                               add_by_user=True)
                profile.city = new_city
            else:
                profile.city = userform.cleaned_data.get('city')
            profile.bio = userform.cleaned_data.get('bio')
            profile.avatar = userform.cleaned_data.get('avatar')
            profile.save()
            return HttpResponseRedirect(reverse('profile', args=[req.user.profile.slug]))
    else:
        userform = SignUp()
    data = {'userform': userform}
    return render(req, 'registration/registration.html', context=data)


@login_required
def afterlogin(req):
    return HttpResponseRedirect(reverse('profile', args=[req.user.profile.slug]))


# def profile(req, user_slug):
#     profile = get_object_or_404(Profile, slug=user_slug)
#     return render(req, 'socialapp/profile_detail.html', context={'profile': profile})


# # class ProfileDetail(generic.DetailView):
#     model = Profile
#     slug_url_kwarg = 'slug'


def profiledetail(req, slug):
    profile = Profile.objects.get(slug=slug)
    subscribtion = profile in req.user.profile.following.all()
    return render(req, 'socialapp/profile_detail.html', context={'profile': profile, 'subscribtion': subscribtion})


@method_decorator(csrf_exempt, name='dispatch')
def subscribe(req):
    if req.POST:
        user_id = req.POST.get('user_id')
        profile_id = req.POST.get('profile_id')
        user = Profile.objects.get(user_id=user_id)
        profile = Profile.objects.get(user_id=profile_id)
        user.following.add(profile)
        print('Подписка оформлена')
        return JsonResponse({'mes': 'Подписка оформлена', 'link': ''})


@method_decorator(csrf_exempt, name='dispatch')
def unsubscribe(req):
    if req.POST:
        user_id = req.POST.get('user_id')
        profile_id = req.POST.get('profile_id')
        user = Profile.objects.get(user_id=user_id)
        profile = Profile.objects.get(user_id=profile_id)
        user.following.remove(profile)
        print('Подписка отменена')
        return JsonResponse({'mes': 'Подписка отменена', 'link': ''})