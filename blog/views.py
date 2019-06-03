from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                    DetailView,CreateView,
                                    UpdateView,DeleteView)
from django.urls import reverse_lazy
from .models import Post,Comment
from .forms import PostForm,CommentForm
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    # this method allows you to modify the content that will be return by PostListView
    # Post is model, .objects specifies all objects(raws) of that model,
    # .filter() allows us to filter the objects we do like in SQLquesries
    # field-name__lte is method that can be called for any field and this is the condition less than or equal to
    # we do have lots of methods like __lte , checkout django section for various methods (field lookups name of section in django doc)
    # we have three main methods of queryset filter(),exclude(),get()
    # order_by() allows you to return all objects in specific order , '-field_name' specifies decending ordere of that field

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

# here we want to login user if they want to create post
# so we have to mix LoginRequired with CreateView class so we imported LoginRequiredMixin
# here login_url defines where to redirect user if user have not loged_in
# and redirect_field_name defines where to redirect user
# form_class defines which form need to show when this CreateView called
class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

# reverse_lazy defines where to go into reverse after we delete the post
# reverse defines where to go but it does not wait to done the task
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')
