from django.contrib.auth.models import User
from django.db.models import Case, When
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic as views
from django.views.generic.base import ContextMixin
from django.template import loader


from django.contrib.auth import mixins as auth_mixins

from devstagram.async_chat.models import ChatRoom, PostMessage
from devstagram.async_chat.utils.room_create import create_room
from devstagram.mainsite.forms import PictureUploadForm, FriendRequestForm, FriendshipForm, PictureUpdateForm, \
    CommentForm, ProfilePictureUploadForm
from devstagram.mainsite.models import Picture, FriendRequest, Like, Friendship, Comment, ProfilePicture, UserFriends

from itertools import chain


def get_pictures():
    queryset= Picture.objects.order_by('-upload_date')
    return queryset


class WelcomePage(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'landing_page.html')


class IndexView(views.ListView):
    template_name = 'index.html'
    context_object_name = 'pictures'

    def get_queryset(self):
        self.queryset = get_pictures()
        return self.queryset


class PictureUploadView(views.CreateView):
    model = Picture
    form_class = PictureUploadForm
    template_name = 'picture_upload.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        picture = form.save(commit=False)
        picture.user = self.request.user
        return super().form_valid(form)


class LikePicture(auth_mixins.LoginRequiredMixin, ContextMixin, views.View):
    def get(self, request, *args, **kwargs):
        picture = Picture.objects.get(pk=kwargs['pk'])
        user_id_list = picture.likes_as_flat_list()
        action = None
        user = request.user
        if user.id not in user_id_list:
            like = Like(picture_id=picture.id, user_id=user.id)
            like.save()
            action = 'like'
        else:
            like = Like.objects.get(picture_id=picture.id, user_id=user.id)
            like.delete()
            action = 'unlike'
        likes = Like.objects.filter(picture_id=picture.id).count()
        # pictures = get_pictures(user)
        pictures = Picture.objects.filter(pk=kwargs['pk'])

        template = loader.render_to_string(
            template_name='index.html',
            context={'pictures': pictures},
            request=self.request, using=None)

        return JsonResponse(data={'template': template,
                                  'context': {
                                            'likes': likes,
                                            'user_id': user.id,
                                            'id_list': list(user_id_list),
                                            'action': action
                                            }
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
        try:
            profile_picture = ProfilePicture.objects.get(user=self.get_object())
        except(Exception) as ex:
            profile_picture = ProfilePicture(user=self.get_object())
            profile_picture.image = 'pictures/default.png'
            profile_picture.save()

        if not self.request.user.is_anonymous:
            friendship = Friendship.objects.filter(friend_one_id=user.id, friend_two_id=request_user.id) | \
                         Friendship.objects.filter(friend_one_id=request_user.id, friend_two_id=user.id)

            is_friend_request_sent = FriendRequest.objects.filter(sender=request_user, receiver=user).exists()
            context['friendship'] = True if friendship else False
            context['is_friend_request_sent'] = is_friend_request_sent

        friends = (Friendship.objects.filter(friend_one=user) | Friendship.objects.filter(
            friend_two=user)).values_list('friend_one_id', 'friend_two_id')
        friends_id = set(chain(*friends))
        if user.id in friends_id:
            friends_id.remove(user.id)

        friends = User.objects.filter(id__in=friends_id)

        context['friends'] = friends
        context['pictures'] = Picture.objects.filter(user=user)
        context['profile_picture'] = profile_picture
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
        pk = kwargs.get('pk')
        picture = Picture.objects.get(pk=pk)
        if request.user.id != picture.user_id:
            raise Http404('Access denied')
        form = PictureUpdateForm(instance=picture)
        context = {'pk': pk, 'form': form, 'picture': picture}
        return render(request, 'picture_edit.html', context)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        picture = Picture.objects.get(pk=pk)
        form = PictureUpdateForm(request.POST, request.FILES, instance=picture)
        if form.is_valid():
            edited_form = form.save(commit=False)
            if not request.FILES:
                edited_form.picture = picture.picture

            edited_form.user_id = request.user.id
            edited_form.save()
            return redirect('index')


class PictureDeleteView(views.DeleteView):
    model = Picture
    template_name = 'picture_display.html'
    success_url = '/index/'

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest('Not allowed')


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
        pk = self.request.POST['pic-pk']
        username = self.get_object().user.username
        print(username, 'username')
        return reverse_lazy('picture display', kwargs={'slug': username, 'pk': pk})


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
        if not request.FILES:
            return redirect('profile', request.user.username)
        if form.is_valid():
            picture = form.save(commit=False)

            old_picture = ProfilePicture.objects.get(user=request.user)
            if not str(old_picture.image).split('/')[1] == 'default.png':
                old_picture.image.delete()

            picture.picture = request.FILES['image']
            picture.user = request.user
            picture.save()
            return redirect('profile', request.user.username)


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
        self.queryset = self.get_users(users)

        # Sort the queryset
        try:
            order = self.request.GET['order']
        except MultiValueDictKeyError:
            order = 'date-joined-asc'
        if order == 'likes-desc':
            return sorted(self.queryset, key=lambda x: -x[1])
        elif order == 'likes-asc':
            return sorted(self.queryset, key=lambda x: x[1])

        elif order == 'posts-asc':
            return sorted(self.queryset, key=lambda x: x[0].picture_set.count())
        elif order == 'posts-desc':
            return sorted(self.queryset, key=lambda x: x[0].picture_set.count(), reverse=True)

        elif 'friends' in order:
            users_ids = [user.id for user in users]
            if order == 'friends-desc':
                userfriends = UserFriends.objects.filter(user_id__in=users_ids).order_by('-friends')
            else:
                userfriends = UserFriends.objects.filter(user_id__in=users_ids).order_by('friends')

            sorted_user_ids = [user.user_id for user in userfriends]
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(sorted_user_ids)])
            users = User.objects.filter(pk__in=sorted_user_ids).order_by(preserved)

        elif order == 'date-joined-desc':
            users = users.order_by('-date_joined')

        elif order == 'date-joined-asc':
            users = users.order_by('date_joined')

        self.queryset = self.get_users(users)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET['q']
        return context


class SendPostViaMessage(views.View):

    def post(self, request, *args, **kwargs):
        pk = int(request.POST['send-to'])
        sender = request.user
        receiver = User.objects.get(pk=pk)
        chatroom = create_room(sender.username, receiver.username)
        chatroom = chatroom['chatroom']
        pic_pk = request.POST['pic-pk']
        picture = Picture.objects.get(pk=pic_pk)
        owner = picture.user
        msg = PostMessage(chatroom=chatroom, sender=sender, post_owner=owner, post_image=picture)
        msg.save()
        chatroom.update_last_msg_time()
        return redirect('index')
