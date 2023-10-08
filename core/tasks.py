# your_app/tasks.py

from celery import shared_task
from django.utils import timezone
from core.models import Post
import requests
import json

# Create celery task


@shared_task
def schedule_and_post_content():
    now = timezone.now()
    scheduled_posts = Post.objects.filter(
        status='schedule',
        scheduled_datetime__lte=now,
    )

    for post in scheduled_posts:
        access_token = post.user.linkedin_access_token
        sub = post.user.linkedin_sub
        if post.media:

            image_file_path = f'/media/{post.media}'

            # Step 1: Register the image for upload
            register_upload_url = 'https://api.linkedin.com/v2/assets?action=registerUpload'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'X-Restli-Protocol-Version': '2.0.0',
                'Content-Type': 'application/json',
            }
            register_upload_data = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": f"urn:li:person:{sub}",
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }
            response = requests.post(register_upload_url, headers=headers, data=json.dumps(register_upload_data))

            if response.status_code == 201:
                upload_url = response.json().get('value', {}).get('uploadMechanism', {}).get(
                    'com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest', {}).get('uploadUrl')
                asset_urn = response.json().get('value', {}).get('asset')
            else:
                print(f"Error registering the image: {response.text}")
                exit()

            # Step 2: Upload the image file
            with open(image_file_path, 'rb') as image_file:
                headers = {
                    'Authorization': f'Bearer {access_token}',
                }
                response = requests.put(upload_url, headers=headers, data=image_file)

            if response.status_code != 200:
                print(f"Error uploading the image: {response.text}")
                exit()

            # Step 3: Create an image share using the asset URN
            image_share_url = 'https://api.linkedin.com/v2/ugcPosts'
            image_share_data = {
                "author": f"urn:li:person:{sub}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": post.content
                        },
                        "shareMediaCategory": "IMAGE",
                        "media": [
                            {
                                "status": "READY",
                                "media": asset_urn,
                            }
                        ]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            response = requests.post(image_share_url, headers=headers, json=image_share_data)

            if response.status_code == 201:
                print("Image share created successfully")
            else:
                print(f"Error creating image share: {response.text}")

        else:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
                'X-Restli-Protocol-Version': '2.0.0',
            }

            data = {
                "author": f"urn:li:person:{sub}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": post.content,
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            response = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, data=json.dumps(data))

            if response.status_code == 201:
                # Share created successfully
                print("Text share created successfully")
            else:
                # Handle error
                print(f"Error creating text share: {response.text}")
        # Update the post status to 'posted'
        post.status = 'posted'
        post.save()
