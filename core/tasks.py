# your_app/tasks.py

from celery import shared_task
from datetime import datetime, timedelta
from core.models import Post  # Import your Post model


# Create celery task
@shared_task
def schedule_and_post_content():
    now = datetime.now()
    scheduled_posts = Post.objects.filter(
        status='schedule',
        scheduled_datetime__lte=now,
    )

    for post in scheduled_posts:
        # Implement the logic to post content to LinkedIn here
        # Example:
        print(f"posted: {post.title}")
        # linkedin_post(post.title, post.content, post.media)

        # After posting, change the post's status to 'posted'
        post.status = 'posted'
        post.save()
