from django.shortcuts import render
from blog_app.models import Post
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import redirect
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_at__isnull=False).order_by("-published_at")
    return render(request,"post_list.html",{"posts":posts})


def post_detail(request,pk):
    # post=Post.objects.get(pk=pk,published_at_isnull=False)
    post = Post.objects.get(pk=pk, published_at__isnull=False)
    return render(
        request,
        "post_detail.html",
        {"post":post},
    )
    
@login_required
def draft_list(request):
    posts=Post.objects.filter(published_at__isnull=True)
    return render(
        request,
        "draft_list.html",
        {"posts":posts}
    )
@login_required
def draft_detail(request,pk):
    # post=Post.objects.get(pk=pk,published_at_isnull=False)
    post = Post.objects.get(pk=pk, published_at__isnull=True)
    return render(
        request,
        "draft_detail.html",
        {"post":post},
    )


@login_required
def draft_publish(request,pk):
     # Corrected query: use __isnull for checking if published_at is NULL
    post = Post.objects.get(pk=pk, published_at__isnull=True)
    post.published_at = timezone.now()  # Set the current date and time
    post.save()  # Save the changes
    return redirect("post-list")  # Redirect to the post list page


def post_create(request):
    if request.method == "GET":
        form = PostForm()
        return render(
            request,
            "post_create.html",
            {"form": form},  # Use 'form' to match the template
        )
    else:  # POST request
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("draft-detail", pk=post.pk)  # Ensure the URL pattern exists
        else:
            return render(
                request,
                "post_create.html",
                {"form": form},  # Ensure consistent key
            )
@login_required
def post_update(request,pk):
    if request.method=="GET":
        post=Post.objects.get(pk=pk)
        form=PostForm(instance=post)
        return render(
            request,
            "post_create.html",
            {"form":form},
        )
    else:
        post=Post.objects.get(pk=pk)
        form=PostForm(request.POST,instance=post)
        if form.is_valid():
            post=form.save()
            if post.published_at:
                return redirect("post-detail",post.pk)
            else:
                return redirect("draft-detail",post.pk)
        else:
            return render(
                request,
                "post_create.html",
                {"form":form},
            )
            
@login_required
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)  # This handles the missing post case
    post.delete()
    return redirect("post-list")  # Redirect to the list of posts or wherever you want
    