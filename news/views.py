from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Vote, Comment, Profile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import PostForm, CategoryForm, CommentForm, RegistrationForm, AvatarForm
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.contrib import messages

def post_list(request):
    sort_by = request.GET.get('sort', 'new')
    query = request.GET.get('q')

    if sort_by == 'new':
        posts = Post.objects.order_by('-created_at')
    elif sort_by == 'positive':
        posts = Post.objects.annotate(positive_votes=Count('votes', filter=models.Q(votes__value=1))).order_by('-positive_votes')
    elif sort_by == 'negative':
        posts = Post.objects.annotate(negative_votes=Count('votes', filter=models.Q(votes__value=-1))).order_by('-negative_votes')
    elif sort_by == 'comments':
        posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    no_results = posts.count() == 0

    for post in posts:
        post.positive_votes = post.votes.filter(value=1).count()
        post.negative_votes = post.votes.filter(value=-1).count()
        post.comments_count = post.comments.count()

    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages) 

    context = {
        'posts': page_obj,
        'sort_by': sort_by,
        'no_results': no_results,
        'page_obj': page_obj  
    }
    return render(request, 'news/post_list.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  
            comment.author = request.user  
            comment.save()
            return redirect('post_detail', post_id=post.id) 
    else:
        form = CommentForm()

    positive_votes = post.votes.filter(value=1).count()
    negative_votes = post.votes.filter(value=-1).count()

    return render(request, 'news/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'positive_votes': positive_votes,
        'negative_votes': negative_votes,
        'comments_count': comments.count(),
        'is_owner': request.user == post.author,
    })

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('post_detail', post_id=post.id) 

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'news/edit_post.html', {
        'form': form,
        'post': post,
    })

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('post_detail', post_id=post.id)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post has been successfully deleted.")
        return redirect('post_list')

    return redirect('post_detail', post_id=post.id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user == comment.author:
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)
    else:
        return redirect('post_detail', post_id=comment.post.id)

def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)

    for post in posts:
        positive_votes = post.votes.filter(value=1).count()
        negative_votes = post.votes.filter(value=-1).count()
        
        post.positive_votes = positive_votes
        post.negative_votes = negative_votes

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'news/category_posts.html', context)

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.creator = request.user
            category.save()
            return redirect('category_list') 
    else:
        form = CategoryForm()
    return render(request, 'news/category_form.html', {'form': form})


@login_required
def vote(request, post_id, vote_type):
    post = get_object_or_404(Post, id=post_id)
    
    if vote_type == 'upvote':
        value = 1
    elif vote_type == 'downvote':
        value = -1
    else:
        return HttpResponseRedirect(reverse('post_detail', args=[post.id])) 

    vote, created = post.votes.get_or_create(user=request.user, defaults={'value': value})

    if not created:
        vote.value = value
        vote.save()

    return HttpResponseRedirect(reverse('post_detail', args=[post.id]))


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'news/post_form.html', {'form': form})

def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    posts = Post.objects.filter(author=user)
    
    posts_count = posts.count()
    comments_count = Comment.objects.filter(author=user).count()
    votes_count = Vote.objects.filter(user=user).count()

    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            compressed_image = profile.compress_image(form.cleaned_data['avatar'])
            resized_image = profile.resize_image(compressed_image)

            profile.avatar = resized_image
            profile.save()
            return redirect('profile', username=user.username) 
    else:
        form = AvatarForm(instance=profile)

    context = {
        'user': user,
        'posts': posts,
        'posts_count': posts_count,
        'comments_count': comments_count,
        'votes_count': votes_count,
        'form': form,  
        'is_own_profile': request.user == user,
        'categories': posts.values('category__name', 'category__id').annotate(post_count=Count('id')),
    }
    
    return render(request, 'news/profile.html', context)

def popular_posts(request):
    one_week_ago = timezone.now() - timedelta(days=7)

    posts = Post.objects.filter(created_at__gte=one_week_ago).annotate(
        total_votes=Sum('votes__value')
    ).order_by('-total_votes')

    for post in posts:
        post.positive_votes = post.votes.filter(value=1).count()
        post.negative_votes = post.votes.filter(value=-1).count()
        post.comments_count = post.comments.count()

    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        return JsonResponse({'html': '', 'has_next': False})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('news/posts_partial.html', {'posts': page_obj})
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next()
        })

    context = {
        'posts': page_obj,
    }
    return render(request, 'news/popular_posts.html', context)

def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'news/category_list.html', context)

def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.user != category.creator:
        return redirect('category_list')  
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'news/category_form.html', {'form': form})

def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.user == category.creator: 
        category.delete()
    
    return redirect('category_list')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list') 
        else:
            return render(request, 'news/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'news/login.html')

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)    
            return redirect('post_list')  
    else:
        form = RegistrationForm()

    return render(request, 'news/register.html', {'form': form})

def logout_view(request):
    logout(request) 
    return redirect('post_list')
