from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post, PostImage
from django.utils import timezone
from .forms import PostForm

def post_list(request):
    # post = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.author = request.user  # ak máš author field
            post.save()

            # Uloží všetky obrázky
            for f in request.FILES.getlist('images'):
                PostImage.objects.create(post=post, image=f)

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

def about_author(request):
    return render(request, 'blog/about_author.html')