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
import datetime
from django.db.models import Q
from django.core.paginator import Paginator


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
            # if userform.cleaned_data.get('city_custom'):
            if userform.cleaned_data.get('city_custom_sign'):
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


# class ProfileDetail(generic.edit.FormMixin, generic.DetailView):
#     model = Profile
#     form_class = PostForm
#     slug_url_kwarg = 'slug'
#
#     def get_success_url(self):
#         return reverse('profile', kwargs={'slug': self.object.slug})
#
#     def get_context_data(self, **kwargs):
#         context = super(ProfileDetail, self).get_context_data(**kwargs)
#         context['form'] = PostForm(initial={'user': self.request.user.id})
#         return context
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         form.save()
#         return super(ProfileDetail, self).form_valid(form)


def profiledetail(req, slug):
    profile = Profile.objects.get(slug=slug)
    # пагинация
    posts = profile.user.post_set.all()
    paginator = Paginator(posts, 10)
    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # новый пост
    postform = PostForm()
    subscribtion = False
    if req.user.username:
        subscribtion = profile in req.user.profile.following.all()
    if req.POST:
        postform = PostForm(req.POST, req.FILES)
        if postform.is_valid():
            # postphoto = req.FILES['photo']
            # file = open('media/' + req.user.username + '/wall' + )
            newpost = Post(text=req.POST['text'], user=req.user, creationdate=datetime.datetime.now())
            newpost.save()
            if postform.cleaned_data['photo']:
                photo = Photo(album='wall', user=req.user, link=postform.cleaned_data['photo'])
                photo.save()
                newpost.photo.add(photo)
            # newpost.save()
            return HttpResponseRedirect(req.path)
    return render(req, 'socialapp/profile_detail.html',
                  context={'profile': profile, 'subscribtion': subscribtion,
                           'form': postform, "page_obj": page_obj})

@login_required()
def delpost(req, id):
    prev_page = req.GET.get('next') if req.GET.get('next') is not None else ''
    post = Post.objects.get(id=id)
    print(post.photo.all()[0].link.storage)
    print(post.photo.all()[0].link.path)
    post.photo.all().delete()
    post.delete()
    return redirect(prev_page) if prev_page else redirect('home')
    # return redirect('../')


@method_decorator(csrf_exempt, name='dispatch')
def subscribe(req):
    if req.POST:
        user_id = req.POST.get('user_id')
        profile_id = req.POST.get('profile_id')
        user = Profile.objects.get(user_id=user_id)
        profile = Profile.objects.get(user_id=profile_id)
        print(user.following.values_list)
        if profile in user.following.all():
            user.following.remove(profile)
            print('Подписка отменена')
        else:
            user.following.add(profile)
            print('Подписка оформлена')
        return JsonResponse({'mes': 'Подписка оформлена', 'link': ''})


class NewsList(generic.ListView):
    model = Post
    template_name = 'socialapp/news.html'

    def get_queryset(self):
        qs = super().get_queryset()
        follow = self.request.user.profile.following.values('user_id')
        return qs.filter(user_id__in=follow) | qs.filter(user_id=self.request.user.id)

@login_required()
def peoplesearch(req):
    profiles = ''
    searchresult = False
    form = PeopleSearchForm()
    if req.POST:
        form = PeopleSearchForm(req.POST)
        if form.is_valid():
            if len(req.POST['query'].split(' ')) > 1:
                query = req.POST['query'].split(' ')
                profiles = Profile.objects.filter(Q(name=query[0], surname=query[1]) |
                                                  Q(name=query[1], surname=query[0]))
            else:
                profiles = Profile.objects.filter(Q(name=req.POST['query']) |
                                                  Q(surname=req.POST['query']) |
                                                  Q(secondname=req.POST['query']) |
                                                  Q(slug=req.POST['query']))
            if profiles:
                searchresult = True
    return render(req, 'socialapp/people.html', context={'form': form, 'profiles': profiles})


class FollowPeopleList(generic.ListView):
    model = Profile
    template_name = 'socialapp/follow_people_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        follow = self.request.user.profile.following.values('user_id')
        return qs.filter(user_id__in=follow)


# class ProfileUpdate(generic.UpdateView):
#     model = Profile
#     form_class = SignUp
#     template_name = 'socialapp/profile_update.html'
#     # fields = ['name', 'surname', 'secondname', 'city', 'birthdate', 'avatar', 'bio']
#     success_url = '/'
#
#     def get_object(self):
#         return self.request.user.profile
#
#     def get_initial(self):
#         initial = super(ProfileUpdate, self).get_initial()
#         initial['name'] = self.request.user.profile.name
#         initial['surname'] = self.request.user.profile.surname
#         initial['secondname'] = self.request.user.profile.secondname
#         initial['city'] = self.request.user.profile.city
#         initial['birthdate'] = self.request.user.profile.birthdate
#         initial['avatar'] = self.request.user.profile.avatar
#         initial['bio'] = self.request.user.profile.bio
#         return initial

@login_required()
def profileupdate(req):
    profile = Profile.objects.get(user_id=req.user.id)
    if req.POST:
        form = ProfileUpdate(req.POST, req.FILES)
        if form.is_valid():
            profile.name = form.cleaned_data.get('name')
            profile.surname = form.cleaned_data.get('surname')
            profile.secondname = form.cleaned_data.get('secondname')
            profile.name = form.cleaned_data.get('name')
            profile.birthdate = form.cleaned_data.get('birthdate')
            if form.cleaned_data.get('city_custom_sign'):
                new_city = City.objects.create(country=form.cleaned_data.get('country'),
                                               name=form.cleaned_data.get('city_custom'),
                                               add_by_user=True)
                profile.city = new_city
            else:
                profile.city = form.cleaned_data.get('city')
            profile.bio = form.cleaned_data.get('bio')
            if form.cleaned_data.get('avatar'):
                profile.avatar = form.cleaned_data.get('avatar')
            profile.save()
        else:
            print(form.errors)
    form = ProfileUpdate(initial={'name': profile.name, 'surname': profile.surname, 'secondname': profile.secondname,
                                  'birthdate': profile.birthdate, 'city': profile.city_id, 'bio': profile.bio,
                                  'avatar': profile.avatar})
    return render(req, 'socialapp/profile_update.html', context={'form': form, 'profile': profile})


def postcomments(req, slug, id):
    post = Post.objects.get(id=id)
    comment_form = PostForm()
    if req.POST:
        comment_form = PostForm(req.POST)
        if comment_form.is_valid():
            Comment.objects.create(text=comment_form.cleaned_data['text'],
                                   post=post,
                                   user=req.user)
    return render(req, 'socialapp/post_comments.html', context={'post': post, 'form': comment_form})