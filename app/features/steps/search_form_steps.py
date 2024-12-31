# features/steps/search_form_steps.py
from behave import given, when, then
from django.test import Client
from app.models import Station, ClassType, Train
from django.urls import reverse
import json



@given("the search form is displayed")
def step_given_search_form_displayed(context):
    context.client = Client()
    context.home_url = reverse("home")
    context.available_train_url = reverse("available_train")

    # Setting up test data
    context.source_station = Station.objects.create(name="Station A")
    context.destination_station = Station.objects.create(name="Station B")
    context.class_type = ClassType.objects.create(name="Economy")

    # Create Train object without assigning the many-to-many field
    train = Train.objects.create(
        name="Test Train",
        source=context.source_station,
        destination=context.destination_station
    )
    # Assign the many-to-many field using .set()
    train.class_type.set([context.class_type])

@when("I submit the form with incomplete information")
def step_when_submit_incomplete_information(context):
    context.response = context.client.get(context.available_train_url, {
        "rfrom": "",  # Missing source
        "to": "",  # Missing destination
        "date": "",  # Missing date
        "ctype": "",  # Missing class type
        "pa": "1",  # Valid number of adults
        "pc": "0",  # Valid number of children
    })

@then("I should see error messages for the required fields")
def step_then_see_error_messages_for_required_fields(context):
    assert context.response.status_code == 302  # Redirect to home page
    messages = list(context.response.wsgi_request._messages)
    assert len(messages) > 0
    assert str(messages[0]) == "Please fillup the form properly"

@when("I submit the form with incorrect information")
def step_when_submit_incorrect_information(context):
    context.response = context.client.get(context.available_train_url, {
        "rfrom": "",  # Invalid source
        "to": "InvalidStation",  # Invalid destination
        "date": "",  # Invalid date
        "ctype": "InvalidClass",  # Invalid class type
        "pa": "0",  # Invalid number of adults (must be at least 1)
        "pc": "0",  # Invalid number of children
    })

@then("I should see error messages for the incorrect fields")
def step_then_see_error_messages_for_incorrect_fields(context):
    assert context.response.status_code == 302  # Redirect to home page
    messages = list(context.response.wsgi_request._messages)
    assert len(messages) > 0
    assert str(messages[0]) == "Please fillup the form properly"

@when("I submit the form with valid information")
def step_when_submit_valid_information(context):
    context.response = context.client.get(context.available_train_url, {
        "rfrom": context.source_station.id,  # Valid source
        "to": context.destination_station.id,  # Valid destination
        "date": "2025-01-03 12:00:00",  # Valid date
        "ctype": context.class_type.id,  # Valid class type
        "pa": "2",  # Valid number of adults
        "pc": "1",  # Valid number of children
    })


@then("I should be redirected to the available trains page")
def step_then_redirected_to_available_trains(context):
    # print("+++++++++++++++++++dalam+++++++++++++++++")
    # print(context.response)
    # Check the status code
    if context.response.status_code == 200:
        # If the page is rendered directly, verify the content
        response_content = context.response.content.decode('utf-8')
        assert "Available Trains" in response_content, "Expected 'Available Trains' in the response content"
        print("Page rendered directly with status code 200")

    elif context.response.status_code in [301, 302]:
        # If the response is a redirect, check the Location header
        redirect_url = context.response['Location']
        print(f"Redirect URL: {redirect_url}")
        expected_url = "/available_train/"  # Replace with the actual URL
        assert redirect_url == expected_url, f"Expected redirect to {expected_url}, but got {redirect_url}"
    
    else:
        # If neither rendering nor redirecting, fail the test
        assert False, f"Unexpected status code: {context.response.status_code}"
    #assert "available_train.html" in [t.name for t in context.response.templates]

