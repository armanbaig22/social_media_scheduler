from django.shortcuts import render, redirect
from urllib.parse import urlencode
import requests
from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from core.models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm
from .models import Post
from .utils import generate_unique_filename, handle_uploaded_file


def frontpage(request):
    return render(request, "base.html")


def login(request):
    return render(request, "login.html")


def linkedin_auth(request):
    # Generate the LinkedIn authorization URL
    params = {
        'response_type': 'code',
        'client_id': settings.LINKEDIN_CLIENT_ID,
        'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
        'state': 'random_string',  # Generate a unique state value
        'scope': 'openid profile w_member_social email',  # Specify the requested scopes
    }
    auth_url = 'https://www.linkedin.com/oauth/v2/authorization?' + urlencode(params)

    return redirect(auth_url)


def linkedin_callback(request):
    # Get the authorization code from the query parameters
    code = request.GET.get('code')
    # Exchange the code for an access token and get user data from LinkedIn
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
        # Store the access token in the user's session
        request.session['linkedin_access_token'] = access_token
        # Fetch user data from LinkedIn
        linkedin_profile_url = 'https://api.linkedin.com/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        linkedin_response = requests.get(linkedin_profile_url, headers=headers)
        print(access_token)
        if linkedin_response.status_code == 200:
            linkedin_data = linkedin_response.json()

            # Extract the user's email address from LinkedIn data
            email = linkedin_data.get('email')
            print(email)
            if email:
                # Check if the user with this email exists in your database
                # Replace 'CustomUser' with your custom user model
                user, created = CustomUser.objects.get_or_create(email=email)

                # Log the user in
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                # Redirect to a success or profile page
                return redirect('profile')
            else:
                # Handle the case where email is missing from LinkedIn data
                return redirect('login')  # Redirect to login page or handle error gracefully
        else:
            # Handle the LinkedIn API response error
            return redirect('login')  # Redirect to login page or handle error gracefully
    else:
        # Handle the error when exchanging code for access token
        return redirect('login')  # Redirect to login page or handle error gracefully


@login_required
def profile(request):
    return render(request, "profile.html")


def logout(request):
    # Retrieve the access token from the user's session
    access_token = request.session.get('linkedin_access_token')

    # Log the user out
    auth_logout(request)

    # Revoke the access token if it exists
    if access_token:
        revoke_token_url = 'https://www.linkedin.com/oauth/v2/revoke'
        revoke_token_params = {
            'token': access_token,
            'client_id': settings.LINKEDIN_CLIENT_ID,
            'client_secret': settings.LINKEDIN_CLIENT_SECRET,
        }
        revoke_response = requests.post(revoke_token_url, data=revoke_token_params)

        # Check if the token revocation was successful
        if revoke_response.status_code == 200:
            # Clear the access token from the user's session
            request.session.pop('linkedin_access_token', None)
            print("Logout successful")
        else:
            print("Logout failed")

    # Redirect to a page after logout, such as the homepage
    return redirect('frontpage')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)

        if form.is_valid():
            # Handle media file upload
            media_file = form.cleaned_data.get('media')
            if media_file:
                # Generate a unique filename for the media file
                unique_filename = generate_unique_filename(media_file.name)
                # Save the media file with the unique filename
                file_path = handle_uploaded_file(media_file)
            else:
                # If no media file is provided, set file_path to None
                file_path = None

            # Create a new Post object
            new_post = Post(
                user=request.user,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['description'],
                media=file_path,
                scheduled_datetime=form.cleaned_data['schedule_datetime'],
                status=form.cleaned_data['post_type'],
                # Add other fields as needed
            )
            new_post.save()
            # Redirect to a success page or do other processing
            return redirect('profile')  # Adjust the redirect URL as needed
    else:
        form = CreatePostForm()

    return render(request, 'create_post.html', {'form': form})


@login_required()
def view_posts(request):
    posts = Post.objects.all()
    return render(request, 'view_posts.html', {'posts': posts})
