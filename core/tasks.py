# your_app/tasks.py

from celery import shared_task
from django.utils import timezone
from core.models import Post


# Create celery task
@shared_task
def schedule_and_post_content():
    now = timezone.now()
    scheduled_posts = Post.objects.filter(
        status='schedule',
        scheduled_datetime__lte=now,
    )

    for post in scheduled_posts:
        # Implement the logic to post content to LinkedIn here

        post.status = 'posted'
        post.save()
