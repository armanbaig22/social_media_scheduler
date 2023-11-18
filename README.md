---

# Project Name
Social Media Scheduler
## Description
Used to schedule the posts on LinkedIn.
## Prerequisites

- Python (version X.X)
- Django (version X.X)
- Redis (version X.X) - For Celery and Celery Beat

## Setup LinkedIn Developer Profile

To integrate your Django application with LinkedIn, you need to set up a LinkedIn Developer Profile. Follow these steps:

1. Visit the LinkedIn Developer portal at [https://developer.linkedin.com](https://developer.linkedin.com).

2. Sign in or create an account if you don't have one.

3. Create a new LinkedIn App by following the instructions on the developer portal.

4. Once you've created the app, you'll receive a Client ID and Client Secret. You'll use these credentials in your Django project.

## Configuration

### Django Configuration

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. In your Django project's settings (`settings.py`), add the LinkedIn API credentials you obtained earlier:

   ```python
   LINKEDIN_CLIENT_ID = 'your-client-id'
   LINKEDIN_CLIENT_SECRET = 'your-client-secret'
   LINKEDIN_REDIRECT_URI = 'http://localhost:8000/auth/linkedin/callback'
   ```

### Celery and Celery Beat Configuration

1. Install and configure Redis:

   - Install Redis (if not already installed).
   - Start the Redis server.

2. In your Django project's settings (`settings.py`), configure Celery and Celery Beat:

   ```python
   # settings.py

   # Celery configuration
   CELERY_BROKER_URL = 'redis://localhost:6379/0'
   CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

   # Celery Beat configuration
   CELERY_BEAT_SCHEDULE = {
       'your-task-name': {
           'task': 'yourapp.tasks.your_task_function',
           'schedule': timedelta(minutes=30),  # Adjust the schedule as needed
       },
   }
   ```

## Running the Application

1. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

2. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

3. Start Celery for background tasks:

   ```bash
   celery -A yourproject worker --loglevel=info
   ```

4. Start Celery Beat for scheduled tasks:

   ```bash
   celery -A yourproject beat --loglevel=info
   ```

5. Access the application in your web browser at [http://localhost:8000](http://localhost:8000).

---

Make sure to replace placeholders (e.g., `your-client-id`, `your-client-secret`, `yourapp.tasks.your_task_function`, `yourproject`) with your actual project-specific values. This README provides a basic outline for setting up your project and configuring LinkedIn integration and Celery tasks. You can expand it with more details, usage instructions, and any other relevant information about your project.
