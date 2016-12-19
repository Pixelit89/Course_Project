import re
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from comment.models import Comment
from comment.forms import CommentForm
from .models import Account, Post, LikeCollector
from .forms import PostForm, EditProfileForm

# Create your views here.


class Index(generic.ListView):
    template_name = 'index.html'

    model = Post

    def get_queryset(self):

        return Post.objects.all().order_by('-pub_date')[:5]


def login_view(request):
    try:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            request.session['id'] = user.id
            return HttpResponseRedirect(reverse_lazy('account', args=(user.id,)))
        else:
            return render(request, 'login.html')
    except:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


def posting(request, account_id):
    if request.POST:
        try:
            new_post = Post(account_id=account_id, post_name=request.POST['post_name'], post=request.POST['post_text'])
            new_post.save()
            return HttpResponseRedirect(reverse('account', args=account_id, ))
        except Post.DoesNotExist:
            return HttpResponse('Error')


class BlogView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    redirect_field_name = ''
    model = Post
    template_name = 'blog.html'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(account_id=self.kwargs['account_id']).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        user = Account.objects.get(id=self.request.session['id'])
        friend = Account.objects.get(id=int(self.kwargs['account_id']))
        context = super(BlogView, self).get_context_data(**kwargs)
        context['friends'] = user.friends.all()
        try:
            context['is_friend'] = user.friends.get(id=friend.id)
        except Account.DoesNotExist:
            context['is_friend'] = None
        context['avatar'] = user.avatar
        context['account_id'] =friend.id
        context['account_name'] = friend.username
        context['post_form'] = PostForm()
        return context


class EditProfile(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login/'
    redirect_field_name = ''
    model = Account
    template_name = 'edit_profile.html'
    form_class = EditProfileForm
    pk_url_kwarg = 'account_id'

    def get_success_url(self):
        return reverse('account', kwargs={'account_id': self.object.pk})


def like_count_blog(request):
    post = Post.objects.get(id=request.GET['post_id'])
    user_id = request.GET['user_name']
    try:
        liked = post.likecollector_set.get(who_liked=user_id)
        post.likecollector_set.remove(liked)
        return HttpResponse(post.likecollector_set.count())
    except LikeCollector.DoesNotExist:
        like = LikeCollector(who_liked=user_id, post_liked=request.GET['post_id'])
        like.save()
        like.post.add(post)
        return HttpResponse(post.likecollector_set.count())


class CommentsView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    redirect_field_name = ''
    model = Comment
    template_name = 'blog_single.html'
    paginate_by = 2

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id']).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(CommentsView, self).get_context_data(**kwargs)
        user = Account.objects.get(id=self.request.session['id'])
        context['friends'] = user.friends.all()
        context['avatar'] = user.avatar
        context['post'] = Post.objects.get(id=self.kwargs['post_id'])
        context['account_id'] = int(self.kwargs['account_id'])
        context['comment_form'] = CommentForm()
        return context


def comment(request, account_id, post_id):
    if request.POST:
        comment = Comment(
            post_id=post_id,
            author=Account.objects.get(id=request.POST['user_id']).username,
            comment_text=request.POST['comment_text']
        )
        comment.save()
        return HttpResponseRedirect(reverse('detail', kwargs={'account_id': account_id, 'post_id': post_id}))


def add_friend(request, account_id):
    user = Account.objects.get(id=request.session['id'])
    friend = Account.objects.get(id=account_id)
    user.friends.add(friend)
    return HttpResponseRedirect(reverse_lazy('account', args=(account_id, )))


def remove_friend(request, account_id):
    user = Account.objects.get(id=request.session['id'])
    friend = Account.objects.get(id=account_id)
    user.friends.remove(friend)
    return HttpResponseRedirect(reverse_lazy('account', args=(account_id, )))


def search(request):
    user = Account.objects.get(id=request.session['id'])
    context = {
        'avatar': user.avatar,
        'account_id': user.id
    }
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q'].strip()
        q = re.compile('[^a-zA-Z ]').sub('', q).split()
        obj = Account.objects
        try:
            first = q[0].capitalize()
            try:
                second = q[1].capitalize()
                q = request.GET['q'].strip()
                names = obj.filter(first_name=first, last_name=second) or \
                    obj.filter(first_name=second, last_name=first) or \
                    obj.filter(first_name=first) or \
                    obj.filter(last_name=second) or \
                    obj.filter(last_name=first) or \
                    obj.filter(first_name=second)
            except (AssertionError, IndexError):
                q = request.GET['q'].strip()
                names = obj.filter(first_name=first) or \
                        obj.filter(username=first)
                if not names:
                    names = obj.filter(last_name=first)
            context.update({'names': names, 'query': q})
            return render(request, 'search.html', context)
        except IndexError:
            return render(request, 'search.html', context)
    return render(request, 'search.html', context)