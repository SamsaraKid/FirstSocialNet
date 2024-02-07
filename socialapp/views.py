from django.contrib.auth.forms import AuthenticationForm
from django.db.models.functions import Lower
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
from django.db.models import Q, Value, When, Case, F, BooleanField, Exists, IntegerField, Subquery
from django.db.models.lookups import GreaterThan, LessThan, Exact
from django.core.paginator import Paginator
import random


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


def communitycreate(req):
    if req.POST:
        form = CommunityCreate(req.POST, req.FILES)
        if form.is_valid():
            community = form.save()
            community.members.add(req.user)
            community.admins.add(req.user, through_defaults={"role": 2})
            return HttpResponseRedirect(reverse('profile', args=[community.slug]))
    else:
        form = CommunityCreate()
    data = {'form': form}
    return render(req, 'registration/community_create.html', context=data)


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


def choisebyslug(req, slug):
    if Profile.objects.filter(slug=slug):
        obj = Profile.objects.get(slug=slug)
        page = profiledetail(req, slug)
    elif Community.objects.filter(slug=slug):
        obj = Community.objects.get(slug=slug)
        page = communitydetail(req, slug)
    return page


def profiledetail(req, slug):
    profile = Profile.objects.get(slug=slug)
    # пагинация
    posts = profile.user.post_set.all().order_by("-creationdate")
    paginator = Paginator(posts, 5)
    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # новый пост
    postform = PostForm()
    if req.user.username:
        subscribtion = profile in req.user.profile.following.all()
    if req.POST:
        postform = PostForm(req.POST, req.FILES)
        if postform.is_valid():
            # postphoto = req.FILES['photo']
            # file = open('media/' + req.user.username + '/wall' + )
            newpost = Post(text=req.POST['text'], user=req.user)
            newpost.save()
            if postform.cleaned_data['photo']:
                photo = Photo(album='wall', user=req.user, link=postform.cleaned_data['photo'])
                photo.save()
                newpost.photo.add(photo)
            # newpost.save()
            return HttpResponseRedirect(req.path)
    return render(req, 'socialapp/profile_detail.html',
                  context={'profile': profile,
                           'form': postform,
                           'page_obj': page_obj})


def communitydetail(req, slug):
    community = Community.objects.get(slug=slug)
    if req.user.username and Communityadminstration.objects.filter(community=community, user_id=req.user.id):
        user_role = Communityadminstration.objects.filter(community=community,
                                                          user_id=req.user.id).values_list('role', flat=True)[0]
    else:
        user_role = -1
    # рандомные пользователи
    num_random_members = 8 if community.members.count() >= 8 else community.members.count()
    id_list = community.members.values_list('id', flat=True)
    random_members = User.objects.filter(id__in=random.sample(list(id_list), num_random_members)).order_by('?')
    # рандомные админы
    num_random_admins = 2 if community.admins.count() >= 2 else community.admins.count()
    id_list = community.admins.values_list('id', flat=True)
    random_admins = User.objects.filter(id__in=random.sample(list(id_list), num_random_admins)).order_by('?')
    # пагинация
    posts = community.post_set.all().order_by("-creationdate")
    paginator = Paginator(posts, 5)
    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # новый пост
    postform = PostForm()
    if req.POST:
        postform = PostForm(req.POST, req.FILES)
        if postform.is_valid():
            # postphoto = req.FILES['photo']
            # file = open('media/' + req.user.username + '/wall' + )
            # print(req.POST['from_community'])
            print(postform.cleaned_data['from_community'])
            newpost = Post(text=postform.cleaned_data['text'], user=req.user, community=community,
                           from_community=postform.cleaned_data['from_community'])
            newpost.save()
            if postform.cleaned_data['photo']:
                photo = Photo(album='wall', user=req.user, link=postform.cleaned_data['photo'], community=community)
                photo.save()
                newpost.photo.add(photo)
            return HttpResponseRedirect(req.path)
    return render(req, 'socialapp/community_detail.html',
                  context={'community': community,
                           'user_role': user_role,
                           'form': postform,
                           'page_obj': page_obj,
                           'random_members': random_members,
                           'random_admins': random_admins,
                           })


def communitymembers(req, slug):
    form = PeopleSearchForm()
    community = Community.objects.get(slug=slug)
    if req.user.username and Communityadminstration.objects.filter(community=community, user_id=req.user.id):
        user_role = Communityadminstration.objects.filter(community=community,
                                                          user_id=req.user.id).values_list('role', flat=True)[0]
    else:
        user_role = -1
    admins = community.admins.all()
    # пагинация
    members = community.members.all()
    paginator = Paginator(members, 5)
    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(req, 'socialapp/members_list.html', context={"page_obj": page_obj,
                                                               'community': community,
                                                               'members': members,
                                                               'user_role': user_role,
                                                               'admins': admins})


def communityadmins(req, slug):
    community = Community.objects.get(slug=slug)
    if req.user.username and Communityadminstration.objects.filter(community=community, user_id=req.user.id):
        user_role = Communityadminstration.objects.filter(community=community,
                                                          user_id=req.user.id).values_list('role', flat=True)[0]
    else:
        user_role = -1
    admins = Communityadminstration.objects.filter(community=community)
    # права на изменение статуса управления
    #                                                                   .annotate(make_owner=Value(False),
    #                                                                              make_admin=Value(False),
    #                                                                              make_moder=Value(False),
    #                                                                              make_del=Value(False))
    # for a in admins:
    #     if user_role == 2 and a.role != 2:
    #         a.make_owner = True
    #     if user_role == 2 and a.role == 0:
    #         a.make_admin = True
    #     if user_role == 2 and a.role == 1:
    #         a.make_moder = True
    #     if user_role > a.role or req.user.id == a.user_id:
    #         a.make_del = True
    # пагинация
    paginator = Paginator(admins, 5)
    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(req, 'socialapp/admins_list.html', context={"page_obj": page_obj,
                                                               'community': community,
                                                               'admins': admins,
                                                               'user_role': user_role})



@login_required()
@method_decorator(csrf_exempt, name='dispatch')
def changeadminstatus(req):
    if req.POST:
        user_id = req.POST.get('user_id')
        user = User.objects.get(id=user_id)
        community_id = req.POST.get('community_id')
        community = Community.objects.get(id=community_id)
        stat = int(req.POST.get('stat'))
        admin = Community.objects.get(id=community_id).communityadminstration_set.filter(user_id=user_id)
        print(admin)
        if stat >= 0:
            if admin:
            # admin = Community.objects.get(id=community_id).communityadminstration_set.get(user_id=user_id)
                admin[0].role = stat
                admin[0].save()
            else:
                community.admins.add(user, through_defaults={"role": stat})
        else:
            Community.objects.get(id=community_id).admins.remove(user)
        mes = f'Статус администратора изменён на {stat}'
        return JsonResponse({'mes': mes, 'link': ''})




@login_required()
def delpub(req, id, type):
    prev_page = req.GET.get('next') if req.GET.get('next') is not None else ''
    if type == 'post':
        post = Post.objects.get(id=id)
        post.photo.all().delete()
        post.delete()
    elif type == 'comment':
        comment = Comment.objects.get(id=id)
        comment.photo.all().delete()
        comment.delete()
    return redirect(prev_page) if prev_page else redirect('home')


@login_required()
@method_decorator(csrf_exempt, name='dispatch')
def like(req):
    if req.POST:
        type = req.POST.get('type')
        if type == 'post':
            model = Post
        elif type == 'comment':
            model = Comment
        elif type == 'photo':
            model = Photo
        id = req.POST.get('id')
        mes = ''
        liked_object = model.objects.get(id=id)
        if req.user in liked_object.like.all():
            liked_object.like.remove(req.user)
            mes = 'Лайк убран'
        else:
            liked_object.like.add(req.user)
            mes = 'Лайк поставлен'
        num_likes = liked_object.count_likes()
        return JsonResponse({'mes': mes, 'link': '', 'num_likes': num_likes})

@method_decorator(csrf_exempt, name='dispatch')
def subscribe(req):
    if req.POST:
        object_id = req.POST.get('object_id')
        type = req.POST.get('type')
        user = Profile.objects.get(user_id=req.user.id)
        if type == 'profile':
            object = Profile.objects.get(user_id=object_id)
            if object in user.following.all():
                user.following.remove(object)
                print('Подписка на пользователя отменена')
            else:
                user.following.add(object)
                print('Подписка на пользователя оформлена')
        elif type == 'community':
            object = Community.objects.get(id=object_id)
            if req.user in object.members.all():
                object.members.remove(req.user)
                print('Подписка на сообщество отменена')
            else:
                object.members.add(req.user)
                print('Подписка на сообщество оформлена')
        return JsonResponse({'mes': 'Подписка оформлена', 'link': ''})


class NewsList(generic.ListView):
    model = Post
    template_name = 'socialapp/news.html'
    paginate_by = 10
    ordering = '-creationdate'

    def get_queryset(self):
        qs = super().get_queryset()
        follow = self.request.user.profile.following.values('user_id')
        return qs.filter(user_id__in=follow) | qs.filter(user_id=self.request.user.id)

# @login_required()
# def peoplesearch(req):
#     profiles = ''
#     searchresult = False
#     page_obj = ''
#     query = ''
#     if not req.GET:
#         req.session['search'] = ''
#         form = PeopleSearchForm()
#     else:
#         form = PeopleSearchForm(req.session['search'])
#     if req.POST:
#         req.session['search'] = req.POST
#         form = PeopleSearchForm(req.session['search'])
#     if req.session['search']:
#         query = req.session['search']['query']
#     if query:
#         if len(query.split(' ')) > 1:
#             query = query.split(' ')
#             profiles = Profile.objects.filter(Q(name__icontains=query[0], surname__icontains=query[1]) |
#                                               Q(name__icontains=query[1], surname__icontains=query[0]))
#         else:
#             profiles = Profile.objects.filter(Q(name__icontains=query) |
#                                               Q(surname__icontains=query) |
#                                               Q(secondname__icontains=query) |
#                                               Q(slug__icontains=query))
#         if profiles:
#             searchresult = True
#             # пагинация
#             paginator = Paginator(profiles, 5)
#             page_number = req.GET.get("page")
#             page_obj = paginator.get_page(page_number)
#     return render(req, 'socialapp/search.html', context={'form': form,
#                                                          'profiles': profiles,
#                                                          'searchresult': searchresult,
#                                                          'page_obj': page_obj,
#                                                          'query': query,
#                                                          })

# @login_required()
# def communitysearch(req):
#     communities = ''
#     searchresult = False
#     page_obj = ''
#     query = ''
#     if not req.GET:
#         req.session['search'] = ''
#         form = CommunitySearchForm()
#     else:
#         form = CommunitySearchForm(req.session['search'])
#     if req.POST:
#         req.session['search'] = req.POST
#         form = CommunitySearchForm(req.session['search'])
#     if req.session['search']:
#         query = req.session['search']['query']
#     if query:
#         communities = Community.objects.filter(Q(title__icontains=req.POST['query']) |
#                                                         Q(communityname__icontains=req.POST['query']))
#         if communities:
#             searchresult = True
#             # пагинация
#             paginator = Paginator(communities, 5)
#             page_number = req.GET.get("page")
#             page_obj = paginator.get_page(page_number)
#     return render(req, 'socialapp/search.html', context={'form': form,
#                                                          'communities': communities,
#                                                          'searchresult': searchresult,
#                                                          'page_obj': page_obj,
#                                                          'query': query,
#                                                          })
    # communities = ''
    # searchresult = False
    # form = CommunitySearchForm()
    # if req.POST:
    #     form = CommunitySearchForm(req.POST)
    #     if form.is_valid():
    #         communities = Community.objects.filter(Q(title__icontains=req.POST['query']) |
    #                                                 Q(communityname__icontains=req.POST['query']))
    #         if communities:
    #             searchresult = True
    # return render(req, 'socialapp/DELETEcommunities.html', context={'form': form, 'communities': communities})


@login_required()
def search(req, type):
    req.session['search_type'] = type
    if req.session['search_type'] == 'user':
        model = Profile
        search_form = PeopleSearchForm
    elif req.session['search_type'] == 'community':
        model = Community
        search_form = CommunitySearchForm
    result = ''
    searchresult = False
    page_obj = ''
    query = ''
    if not req.GET:
        req.session['search'] = ''
        form = search_form()
    else:
        form = search_form(req.session['search'])
    if req.POST:
        req.session['search'] = req.POST
        form = search_form(req.session['search'])
    if req.session['search']:
        query = req.session['search']['query']
    if query:
        if req.session['search_type'] == 'user':
            if len(query.split(' ')) > 1:
                query = query.split(' ')
                result = model.objects.filter(Q(name__icontains=query[0], surname__icontains=query[1]) |
                                                  Q(name__icontains=query[1], surname__icontains=query[0]))
            else:
                result = model.objects.filter(Q(name__icontains=query) |
                                                  Q(surname__icontains=query) |
                                                  Q(secondname__icontains=query) |
                                                  Q(slug__icontains=query))
        elif req.session['search_type'] == 'community':
            result = model.objects.filter(Q(title__icontains=req.POST['query']) |
                                                   Q(communityname__icontains=req.POST['query']))
        if result:
            searchresult = True
            # пагинация
            paginator = Paginator(result, 5)
            page_number = req.GET.get("page")
            page_obj = paginator.get_page(page_number)
    return render(req, 'socialapp/search.html', context={'form': form,
                                                         'result': result,
                                                         'searchresult': searchresult,
                                                         'page_obj': page_obj,
                                                         'query': query,
                                                         'type': req.session['search_type']
                                                         })



class FollowPeopleList(generic.ListView):
    model = Profile
    template_name = 'socialapp/follow_people_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        follow = self.request.user.profile.following.values('user_id')
        return qs.filter(user_id__in=follow)



def communitylist(req):
    subscriber = req.user.member.all()
    admin = req.user.admin.all()
    queryset = admin.union(subscriber)
    return render(req, 'socialapp/follow_community_list.html', context={'communities': queryset})



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
                profile.avatar.delete()
                profile.avatar = form.cleaned_data.get('avatar')
                profile.save()
            profile.save()
        else:
            print(form.errors)
    form = ProfileUpdate(initial={'name': profile.name, 'surname': profile.surname, 'secondname': profile.secondname,
                                  'birthdate': profile.birthdate, 'city': profile.city_id, 'bio': profile.bio,
                                  'avatar': profile.avatar})
    return render(req, 'socialapp/profile_update.html', context={'form': form, 'profile': profile})


def postcomments(req, slug, id):
    post = Post.objects.get(id=id)
    community = post.community
    if req.user.username and Communityadminstration.objects.filter(community=community, user_id=req.user.id) and community:
        user_role = Communityadminstration.objects.filter(community=community,
                                                          user_id=req.user.id).values_list('role', flat=True)[0]
    else:
        user_role = -1
    comment_form = PostForm()
    # пагинация
    num_comments_on_page = 5
    comments = post.comment_set.all()
    paginator = Paginator(comments, num_comments_on_page)
    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if req.POST:
        comment_form = PostForm(req.POST, req.FILES)
        if comment_form.is_valid():
            newcomment = Comment.objects.create(text=comment_form.cleaned_data['text'],
                                                post=post,
                                                user=req.user,
                                                from_community=comment_form.cleaned_data['from_community'])
            if comment_form.cleaned_data['photo']:
                photo = Photo.objects.create(album='comments',
                                             link=comment_form.cleaned_data['photo'],
                                             user=req.user)
                newcomment.photo.add(photo)
            if len(post.comment_set.values()) % 5 == 1 and len(post.comment_set.values()) > 1:
                num_last_page = paginator.num_pages + 1
            else:
                num_last_page = paginator.num_pages
            print(req.path, paginator.num_pages)
            return redirect(req.path + ('?page=' + str(num_last_page) if len(post.comment_set.values()) > 5 else ''))
    return render(req, 'socialapp/post_comments.html', context={'post': post,
                                                                'form': comment_form,
                                                                "page_obj": page_obj,
                                                                'user_role': user_role})

