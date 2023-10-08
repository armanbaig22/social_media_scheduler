from django.shortcuts import render, redirect, get_object_or_404
from urllib.parse import urlencode
import requests
from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from core.models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm, PostForm
from .models import Post
from .utils import generate_unique_filename, handle_uploaded_file


def frontpage(request):
    return render(request, "base.html")


def login(request):
    return render(request, "login.html")


def linkedin_auth(request):

    params = {
        'response_type': 'code',
        'client_id': settings.LINKEDIN_CLIENT_ID,
        'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
        'state': 'random_string',
        'scope': 'openid profile w_member_social email',
    }
    auth_url = 'https://www.linkedin.com/oauth/v2/authorization?' + urlencode(params)

    return redirect(auth_url)


def linkedin_callback(request):
    code = request.GET.get('code')
    token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    token_params = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': settings.LINKEDIN_CLIENT_ID,
        'client_secret': settings.LINKEDIN_CLIENT_SECRET,
        'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
    }

    response = requests.post(token_url, data=token_params)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        request.session['linkedin_access_token'] = access_token
        linkedin_profile_url = 'https://api.linkedin.com/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        linkedin_response = requests.get(linkedin_profile_url, headers=headers)
        if linkedin_response.status_code == 200:
            linkedin_data = linkedin_response.json()

            email = linkedin_data.get('email')
            if email:

                user, created = CustomUser.objects.get_or_create(email=email)

                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                return redirect('profile')
            else:
                return redirect('login')
        else:
            return redirect('login')
    else:
        return redirect('login')


@login_required
def profile(request):
    return render(request, "profile.html")


def logout(request):

    access_token = request.session.get('linkedin_access_token')
    auth_logout(request)

    if access_token:
        revoke_token_url = 'https://www.linkedin.com/oauth/v2/revoke'
        revoke_token_params = {
            'token': access_token,
            'client_id': settings.LINKEDIN_CLIENT_ID,
            'client_secret': settings.LINKEDIN_CLIENT_SECRET,
        }
        revoke_response = requests.post(revoke_token_url, data=revoke_token_params)

        if revoke_response.status_code == 200:
            request.session.pop('linkedin_access_token', None)
            print("Logout successful")
        else:
            print("Logout failed")

    return redirect('frontpage')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)

        if form.is_valid():
            media_file = form.cleaned_data.get('media')
            if media_file:
                unique_filename = generate_unique_filename(media_file.name)
                file_path = handle_uploaded_file(media_file)
            else:
                file_path = None

            new_post = Post(
                user=request.user,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['description'],
                media=file_path,
                scheduled_datetime=form.cleaned_data['schedule_datetime'],
                status=form.cleaned_data['post_type'],
            )
            new_post.save()
            return redirect('profile')
    else:
        form = CreatePostForm()

    return render(request, 'create_post.html', {'form': form})


@login_required()
def view_posts(request):
    user = request.user
    scheduled_posts = Post.objects.filter(user=user, status__in=['draft', 'schedule'])

    context = {
        'scheduled_posts': scheduled_posts
    }

    return render(request, 'view_posts.html', context)


def modify_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('view_posts')
    else:
        form = PostForm(instance=post)

    return render(request, 'modify_post.html', {'form': form, 'post': post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('view_posts')

    return render(request, 'delete_post.html', {'post': post})
