# Auto Pilot

Auto Pilot is a Django-based web application that is used to Schedule posts for later time

## Features

- LinkedIn OAuth 2.0 authentication.
- User profile creation based on LinkedIn data.
- Secure user authentication.
- Customizable templates and styles for seamless integration into your project.
- An easy-to-follow structure for extending functionality.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system.
- Django framework and other project dependencies installed. You can install them using:

    ```bash
    pip install -r requirements.txt
    ```

- LinkedIn Developer Account: You'll need to create a LinkedIn Developer account and set up your application to obtain the client ID and client secret for LinkedIn OAuth 2.0 authentication.

## Configuration

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/your-username/auto-pilot.git
    cd auto-pilot
    ```

2. Create a `.env` file in the project root directory and add your LinkedIn API credentials:

    ```env
    LINKEDIN_CLIENT_ID=your-linkedin-client-id
    LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
    LINKEDIN_REDIRECT_URI=your-redirect-uri
    ```

3. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

## Running the Application

4. Start the development server:

    ```bash
    python manage.py runserver
    ```

5. Access the application in your web browser at `http://localhost:8000`.

## LinkedIn Authentication

6. Click on the "Login with LinkedIn" button to initiate the LinkedIn authentication process.

7. After successful authentication, you will be redirected to your profile page.

## Logging Out

8. To log out, click on the "Logout" button.

## Customization

You can customize the project to fit your specific needs by modifying the templates, views, and stylesheets provided in the project directory.

## Contributing

If you would like to contribute to this project or report issues, please follow our [Contributing Guidelines](CONTRIBUTING.md).

