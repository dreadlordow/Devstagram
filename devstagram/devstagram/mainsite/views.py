from django.contrib.auth.models import User
from django.db.models import Case, When
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic as views

from django.contrib.auth import mixins as auth_mixins

from devstagram.mainsite.forms import PictureUploadForm, FriendRequestForm, FriendshipForm, PictureUpdateForm, \
    CommentForm, ProfilePictureUploadForm, SortingForm
from devstagram.mainsite.mixins.notificationmixin import NotificationMixin
from devstagram.mainsite.models import Picture, FriendRequest, Like, Friendship, Comment, ProfilePicture, UserFriends

from itertools import chain


class IndexView(views.ListView):
    template_name = None
    context_object_name = 'pictures'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.template_name = 'landing_page.html'
        else:
            self.template_name = 'index.html'
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if not user.is_anonymous:
            friends = (Friendship.objects.filter(friend_one=user) | Friendship.objects.filter(
                friend_two=user)).values_list('friend_one_id', 'friend_two_id')
            friends = set(chain(*friends))
            friends.add(user)
            self.queryset = Picture.objects.filter(user_id__in=friends).order_by('-upload_date')
            return self.queryset


class PictureUploadView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = Picture
    form_class = PictureUploadForm
    template_name = 'picture_upload.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        picture = form.save(commit=False)
        picture.user = self.request.user
        return super().form_valid(form)


class LikePicture(auth_mixins.LoginRequiredMixin,NotificationMixin ,views.View):
    def get(self, request, *args, **kwargs):
        picture = Picture.objects.get(pk=kwargs['pk'])
        user = request.user
        user_id_list = picture.likes_as_flat_list()
        action = None
        if user.id not in user_id_list:
            like = Like(picture_id=picture.id, user_id=user.id)
            like.save()
            action = 'like'
        else:
            like = Like.objects.get(picture_id=picture.id, user_id=user.id)
            like.delete()
            action = 'unlike'
        likes = Like.objects.filter(picture_id=picture.id).count()

        return JsonResponse(data={
            'likes': likes,
            'user_id': user.id,
            'id_list': list(user_id_list),
            'action': action,
        })


class ProfileView(views.DetailView):
    model = User
    template_name = 'profile.html'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        request_user = self.request.user
        profile_picture = ProfilePicture.objects.get(user=self.get_object())
        friendship = Friendship.objects.filter(friend_one_id=user.id, friend_two_id=request_user.id) | \
                     Friendship.objects.filter(friend_one_id=request_user.id, friend_two_id=user.id)

        is_friend_request_sent = FriendRequest.objects.filter(sender=request_user, receiver=user).exists()
        friends = (Friendship.objects.filter(friend_one=user) | Friendship.objects.filter(
            friend_two=user)).values_list('friend_one_id', 'friend_two_id')
        friends_id = set(chain(*friends))
        if user.id in friends_id:
            friends_id.remove(user.id)

        friends = User.objects.filter(id__in=friends_id)

        context['friends'] = friends
        context['pictures'] = Picture.objects.filter(user=user)
        context['friendship'] = True if friendship else False
        context['profile_picture'] = profile_picture
        context['is_friend_request_sent'] = is_friend_request_sent


        return context


class FriendRequestView(auth_mixins.LoginRequiredMixin, views.View):
    template_name = 'profile.html'
    success_url = 'index'

    def post(self, request, *args, **kwargs):
        form = FriendRequestForm()
        fr = form.save(commit=False)
        sender = User.objects.get(username=request.POST['sender'])
        receiver = User.objects.get(username=request.POST['receiver'])
        try:
            friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
            friend_request.delete()

        except FriendRequest.DoesNotExist:
            fr.sender = sender
            fr.receiver_id = receiver.id
            fr.save()
        return redirect('profile', receiver)


class CreateFriendship(views.View):
    template_name = 'profile.html'

    def post(self, request, *args, **kwargs):
        form = FriendshipForm()
        friendship = form.save(commit=False)
        sender_username = request.POST['sender']
        receiver_username = request.POST['receiver']
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        sender_friends, created = UserFriends.objects.get_or_create(user=sender)
        receiver_friends, created = UserFriends.objects.get_or_create(user=receiver)

        if request.POST['answer'] == 'accepted':
            friendship.friend_one = sender
            friendship.friend_two = receiver
            friendship.save()
            sender_friends.friends += 1
            receiver_friends.friends += 1
            sender_friends.save()
            receiver_friends.save()

        request_to_remove = FriendRequest.objects.get(sender=sender, receiver=receiver)
        request_to_remove.delete()

        return redirect('index')


class PictureDisplayView(views.DetailView):
    model = Picture
    template_name = 'picture_display.html'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        picture = Picture.objects.get(pk=self.kwargs.get('pk'))
        return picture

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        picture = self.get_object()
        form = CommentForm()
        comments = Comment.objects.filter(picture_id=picture.id)
        context['picture'] = picture
        context['form'] = form
        context['comments'] = comments
        return context


class PictureEditView(views.View):

    def get(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk')
        self.picture = Picture.objects.get(pk=self.pk)
        if request.user.id != self.picture.user_id:
            raise Http404('Access denied')
        form = PictureUpdateForm(instance=self.picture)
        context = {'pk': self.pk, 'form': form}
        return render(request, 'picture_edit.html', context)

    def post(self, request, *args, **kwargs):
        form = PictureUpdateForm(request.POST, request.FILES, instance=self.picture)

        if form.is_valid():
            edited_form = form.save(commit=False)

            if not request.FILES:
                edited_form.picture = self.picture.picture

            edited_form.user_id = request.user.id
            edited_form.save()
            return redirect('index')


class CommentPictureView(auth_mixins.LoginRequiredMixin, views.View):
    template_name = 'picture_display.html'

    def post(self, request, *args, **kwargs):
        picture_id = request.POST['pic_id']
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.user = request.user
        comment.picture_id = picture_id
        comment.save()

        picture = Picture.objects.get(pk=picture_id)
        comments = Comment.objects.filter(picture_id=picture.id)
        context = {
            'form': CommentForm,
            'comments': comments,
            'picture': picture
        }
        return redirect('picture display', picture.user, picture_id)


class DeleteCommentView(views.DeleteView):
    model = Comment

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        username = self.get_object().user.username
        return reverse_lazy('picture display', kwargs={'slug': username, 'pk':pk})


class ProfilePictureUploadView(views.View):
    template_name = 'profile_picture.html'

    def get(self, request, *args, **kwargs):
        current_picture = ProfilePicture.objects.get(user=request.user)
        form = ProfilePictureUploadForm()
        context = {
            'form': form,
            'currentpfp': current_picture
        }

        return render(request, 'profile_picture.html', context)

    def post(self, request, *args, **kwargs):
        current_picture = ProfilePicture.objects.get(user=request.user)
        form = ProfilePictureUploadForm(request.POST, request.FILES, instance=current_picture)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.picture = request.FILES['image']
            picture.user = request.user
            picture.save()
            return redirect('profile', request.user.username)

#
# class SearchView(views.View):
#     def get(self, request, *args, **kwargs):
#         search = request.GET['q']
#         users = User.objects.filter(username__icontains=search)
#         all_likes = []
#         for user in users:
#             likes = 0
#             for pic in user.picture_set.all():
#                 likes += len(pic.likes_as_flat_list())
#             all_likes.append(likes)
#         zipped_list = sorted(list(zip(users, all_likes)), key=lambda x:x[1])
#         print(zipped_list)
#         context = {'searched_users_all_likes':zipped_list, 'q': search}
#         return render(request, 'search.html', context)


class SearchView(views.ListView):
    template_name = 'search.html'
    context_object_name = 'searched_users_all_likes'

    def get_users(self, users):
        all_likes = []
        for user in users:
            likes = 0
            for pic in user.picture_set.all():
                likes += len(pic.likes_as_flat_list())
            all_likes.append(likes)
        zipped_list = list(zip(users, all_likes))
        return zipped_list

    def get_queryset(self):
        search = self.request.GET['q']
        users = User.objects.filter(username__icontains=search)

        # Sort the queryset
        try:
            order = self.request.GET['order']
            if order == 'likes-asc':
                self.queryset = sorted(self.queryset, key=lambda x: -x[1])
            elif order == 'likes-desc':
                self.queryset = sorted(self.queryset, key=lambda x: x[1])
            elif 'friends' in order:
                users_ids = [user.id for user in users]
                if order == 'friends-asc':
                    userfriends = UserFriends.objects.filter(user_id__in=users_ids).order_by('-friends')
                else:
                    userfriends = UserFriends.objects.filter(user_id__in=users_ids).order_by('friends')
                sorted_user_ids = [user.user_id for user in userfriends]
                preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(sorted_user_ids)])
                users = User.objects.filter(pk__in=sorted_user_ids).order_by(preserved)
            elif order == 'date-joined-asc':
                users = users.order_by('-date_joined')
            else:
                users = users.order_by('date_joined')

        except MultiValueDictKeyError:
            pass

        zipped_list = self.get_users(users)
        return zipped_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET['q']
        return context