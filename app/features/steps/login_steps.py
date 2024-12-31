from behave import given, when, then
from django.test import Client
from django.urls import reverse

@given("I am on the login page")
def step_on_login_page(context):
    context.client = Client()
    context.response = context.client.get(reverse('login'))
    assert context.response.status_code == 200

@when("I enter valid credentials")
def step_enter_valid_credentials(context):
    context.response = context.client.post(reverse('login'), {
        'username': 'zari',  # Replace with a valid username
        'password': '123456789'  # Replace with the correct password
    })

@when("I enter invalid credentials")
def step_enter_invalid_credentials(context):
    context.response = context.client.post(reverse('login'), {
        'username': 'zari',
        'password': '987654321'
    })

@when("I click the login button")
def step_click_login_button(context):
    # This step is handled in the POST requests above.
    pass

@then("I should be redirected to the dashboard")
def step_redirect_to_dashboard(context):
    assert context.response.status_code == 302  # 302 indicates a redirect
    assert context.response.url == reverse('home')  # Replace 'home' with your dashboard URL name

@then("I should see an error message")
def step_see_error_message(context):
    response = context.client.get(context.response.url, follow=True)

    # Access messages from the session
    from django.contrib.messages import get_messages
    storage = get_messages(response.wsgi_request)

    # Convert messages to a list for easier validation
    messages = [str(message) for message in storage]

    # Debug the messages (optional)
    print(f"Messages: {messages[0]}")

    assert "Incorrect username or password" in messages[0]
