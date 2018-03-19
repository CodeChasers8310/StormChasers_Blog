from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .models import top_post, response_post
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'blog/home.html')

@login_required
def dashboard(request):
    return render(request, 'blog/dashboard.html')

@login_required
def locations(request):
    return render(request, 'blog/locations.html')

@login_required
def blog(request):
    return render(request, 'blog/blog.html')

@login_required
def my_profile(request):
    return render(request, 'blog/my_profile.html')

def about_us(request):
    return render(request, 'blog/about_us.html')

@login_required
def subscriptions(request):
    return render(request, 'blog/subscriptions.html')

'''Uses old django girls post object
@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    return render(request, 'blog/post_list.html', {'posts': posts})
'''

'''Uses old django girls post object
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
'''

'''Uses old django girls post object
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
'''

'''Uses old django girls post object
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
'''
