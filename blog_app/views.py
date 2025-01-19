from django.shortcuts import render, redirect
from blog_app.models import Post

from django.utils import timezone
from .forms import PostForm
from django.views.generic import ListView, DetailView, UpdateView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    
    def get_queryset(self):
        # Fetching only published posts
        posts = Post.objects.filter(published_at__isnull=False).order_by("-published_at")
        return posts

class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    
    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=False)
        return queryset


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "draft_list.html"
    context_object_name = "posts"
    
    def get_queryset(self):
        queryset = Post.objects.filter(published_at__isnull=True)
        return queryset

class DraftDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "draft_detail.html"
    context_object_name = "post"
    
    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=True)
        return queryset
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_create.html"  # Adjusted template for post creation
    form_class = PostForm
    success_url = reverse_lazy("post-list")  # Default redirect to post list

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        # Redirect to the post-update page for the newly created post
        return redirect('post-update', pk=post.pk)


class DraftPublishView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, published_at__isnull=True)
            post.published_at = timezone.now()
            post.save()
            return redirect("post-list")
        except ObjectDoesNotExist:
            # Handle case when the post does not exist or is not a draft
            return redirect("draft-list")  # Redirect to the draft list page if not found


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "post_create.html"  # Same template for create and update (or you can use a separate one)
    form_class = PostForm
    
    def get_success_url(self):
        post = self.get_object()
        if post.published_at:
            return reverse_lazy("post-detail", kwargs={"pk": post.pk})
        else:
            return reverse_lazy("draft-detail", kwargs={"pk": post.pk})



class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,pk):
        post=Post.objects.get(pk=pk)
        post.delete()
        return redirect("post-list")

