from social_core.pipeline.user import user_details


def save_instagram_user(backend, user, response, *args, **kwargs):
    if backend.name == 'instagram':

        instagram_user_id = response['id']
        username = response['username']
        email = response.get('email', '')  # Instagram may not provide email

        # Update or create the user in your database
        user.username = username
        user.email = email
        user.save()


