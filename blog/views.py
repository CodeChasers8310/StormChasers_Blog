from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .models import top_post, response_post
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory
from .forms import ImageForm, PostForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import top_post, response_post, image
from .models import image as dbimage
from .forms import PostForm, ImageForm
from random import randrange
from django.contrib import messages


''' Before multi-form - this is only one image at a time
# @login_required
# def new_top_post(request):
#     # Handle file upload
#     if request.method == 'POST':
#         # Use prefixes to get different parts of the form
#         imageForm = ImageForm(request.POST, request.FILES, prefix='ImageForm')
#         postForm = PostForm(request.POST, prefix='PostForm')
#         # Only proceed if both forms are valid
#         if imageForm.is_valid() and postForm.is_valid():
#             title = request.POST['PostForm-title']
#             text = request.POST['PostForm-title']
#             newTopPost = top_post(title=title,
#                                   text=text,
#                                   created_date=timezone.now(),
#                                   published_date=timezone.now(),
#                                   user_id=request.user,)
#             newTopPost.save()
#
#             # This needs to reference the above top post object
#             topPostInstance = get_object_or_404(top_post, post_id=newTopPost.post_id)
#             newImage = image(image = imageForm.cleaned_data['image'], top_post_id=topPostInstance)
#             newImage.save()
#
#             # Redirect to the document list after POST
#             return redirect('post_detail', post_id=newTopPost.post_id)
#             # return redirect('blog/blog.html', blog_id=newTopPost.post_id)
#         else:
#             return render(request,'blog/blog.html',)
#     else:
#         # Use prefixes to label different parts of the form
#         imageForm = ImageForm(prefix="ImageForm")
#         postForm = PostForm(prefix="PostForm")
#
#     # Load documents for the list page
#     # Ghetto testing if you want to pass this to template
#     #images = image.objects.all()
#
#     # Render list page with the documents and the form
#     return render (request,
#         'blog/new_post.html',
#         {'imageForm': imageForm, 'postForm':postForm},
#     )
'''

@login_required
def new_top_post(request):

    ImageFormSet = modelformset_factory(dbimage,
                                        form=ImageForm, extra=10)

    if request.method == 'POST':
        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=dbimage.objects.none())


        if postForm.is_valid() and formset.is_valid():
            print(request.POST)
            title = request.POST['title']
            text = request.POST['text']
            newTopPost = top_post(title=title,
                                  text=text,
                                  created_date=timezone.now(),
                                  published_date=timezone.now(),
                                  user_id=request.user,)
            newTopPost.save()
            # Get object to save with images
            topPostInstance = get_object_or_404(top_post, post_id=newTopPost.post_id)
            print(formset.cleaned_data)

            for form in formset.cleaned_data:
                try:
                    image = form['image']
                    photo = dbimage(image = image, top_post_id=topPostInstance)
                    photo.save()
                except KeyError:
                    pass
            return HttpResponseRedirect(reverse('blog'))
        else:
            print (postForm.errors, formset.errors)
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=dbimage.objects.none())
    return render(request, 'blog/new_post.html',
                  {'postForm': postForm, 'formset': formset})

@login_required
def post_deleted(request, id):
    print(id)
    post = top_post.objects.get(post_id=id).delete()
    return render(request, 'blog/post_deleted_after.html')
    # return HttpResponseRedirect(reverse('post_deleted'))#, kwargs={'id':id}))

@login_required
def post_detail(request, post_id):
    topPost = get_object_or_404(top_post, post_id=post_id)
    images = image.objects.filter(top_post_id=topPost.post_id)
    return render(request, 'blog/post_detail.html', {'post': topPost, 'images':images})

@login_required
def delete_image(request, id):
    # Get the ID for the page to redirect to after deletion
    postId = image.objects.get(id=id)
    postId = postId.top_post_id.post_id
    images = image.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('post_edit', kwargs={'post_id':postId}))

@login_required
def post_edit(request, post_id):
    topPost = get_object_or_404(top_post, post_id=post_id)
    # Need to lay these out in an editable way
    images = image.objects.filter(top_post_id=topPost.post_id)
    if request.method == "POST":
        postForm = PostForm(request.POST, prefix='PostForm')
        if postForm.is_valid():
            title = request.POST['PostForm-title']
            text = request.POST['PostForm-title']
            newTopPost = top_post(title=title,
                                  text=text,
                                  created_date=timezone.now(),
                                  published_date=timezone.now(),
                                  user_id=request.user,)
            newTopPost.save()
            return redirect('post_detail', post_id=newTopPost.post_id)
    else:
        form = PostForm(instance=topPost, prefix='PostForm')
        #images = ImageForm()
        return render(request, 'blog/post_edit.html', {'form': form, 'images':images})

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
    topPosts = top_post.objects.all().order_by('-post_id')
    displayImages = []
    # Get some default image if posts don't have an image
    defaultImage = None#image.objects.get(image='blogImages/2018/03/20/instructor.jpg')
    for post in topPosts:
        allBlogImages = image.objects.filter(top_post_id=post.post_id)
        try:
            randomImage = allBlogImages[randrange(0, len(allBlogImages))]
        except:
            randomImage = defaultImage
        displayImages.append(randomImage)
    return render(request, 'blog/blog.html', {'topPosts':topPosts, 'blogImages':displayImages})

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
