from behave import given, when, then
from django.contrib.auth import get_user_model
from django.test import Client
from django.contrib.messages import get_messages
from app.models import Feedback
from django.contrib.auth import logout


@given('the user is logged in')
def step_impl(context):
    context.client = Client()  # Initialize the test client
    User = get_user_model()  # Get the custom user model
    email = 'testuser1@example.com'
    username = 'testuser'
    password = 'testpassword'
    
    # Check if the user already exists to avoid duplicate creation
    context.user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email}
    )
    
    # Ensure the password is set properly
    if not created:
        context.user.set_password(password)
        context.user.save()
    
    # Log the user in
    login_successful = context.client.login(username=username, password=password)
    assert login_successful, "Failed to log in the test user"


@given('the user is not logged in')
def step_impl(context):
    context.client = Client()  # Initialize the test client
    # Log out the user if they are logged in
    if context.client.session:
        logout(context.client)
    print("User logged out. Session state:", context.client.session.items())


@given('the user is on the feedback submission page')
def step_impl(context):
    context.response = context.client.get('/feedback')  # Use the correct feedback page URL
    assert context.response.status_code == 200, "Failed to load the feedback submission page"


@when('the user submits valid feedback')
def step_impl(context):
    context.response = context.client.post('/feedback', {'feedback': 'This is a valid feedback'})  # Submit valid feedback
    assert context.response.status_code in [200, 302], "Feedback submission failed"


@when('the user submits invalid feedback')
def step_impl(context):
    context.response = context.client.post('/feedback', {'feedback': ''})  # Submit invalid feedback
    assert context.response.status_code == 302, "Invalid feedback did not reload the page"


@when('the user tries to access the feedback submission page')
def step_impl(context):
    context.response = context.client.post('/feedback', {'feedback': 'Test feedback'})
    # print("Response status code:", context.response.status_code)
    # print("Response content:", context.response.content.decode())


@then('the feedback is successfully submitted')
def step_impl(context):
    # Check the feedback count before and after submission
    initial_count = Feedback.objects.count()
    context.response = context.client.post('/feedback', {'feedback': 'This is a valid feedback'})  # Submit valid feedback
    final_count = Feedback.objects.count()
    assert final_count == initial_count + 1, f"Expected feedback count to increment by 1, but got {final_count - initial_count}"
    
    # Verify the most recent feedback's content
    feedback = Feedback.objects.latest('id')  # Get the most recent feedback
    assert feedback.feedback == 'This is a valid feedback', "Feedback content does not match"
    assert feedback.name == f"{context.user.first_name} {context.user.last_name}", "Feedback user name does not match"


@then('a confirmation message is displayed')
def step_impl(context):
    # Access messages from the session
    response = context.client.get(context.response.url, follow=True)
    storage = get_messages(response.wsgi_request)
    messages = [str(message) for message in storage]
    
    # Debug the messages (optional)
    print(f"Messages: {messages[0]}")
    
    # Check if the confirmation message is present
    assert "Thanks for your feedback!" in messages[0], "Confirmation message not displayed"


@then('the system displays an error message indicating the invalid feedback')
def step_impl(context):
    # Access messages from the session
    response = context.client.get(context.response.url, follow=True)
    storage = get_messages(response.wsgi_request)
    messages = [str(message) for message in storage]
    
    # Debug the messages (optional)
    print(f"Messages: {messages[0]}")
    
    # Check if the error message is present
    assert "please write something first and then submit feedback" in messages[0], "Error message not displayed for invalid feedback"


@then('the user sees an error message indicating they need to log in')
def step_impl(context):
    # Follow the redirect if it exists
    if context.response.status_code == 302:  # Redirect status code
        redirect_response = context.client.get(context.response.url, follow=True)
        storage = get_messages(redirect_response.wsgi_request)
    else:
        storage = get_messages(context.response.wsgi_request)

    # Extract messages
    messages = [str(message) for message in storage]

    # Debugging messages (optional)
    print(f"Messages: {messages}")

    # Assert the expected message is present
    assert "Please login first to post feedback." in messages, "Error message for not being logged in not displayed"
