from behave import given, when, then
from django.test.client import Client
from app.models import Ticket
from datetime import time

# Initialize Django test client
client = Client()

@given('I have a valid ticket in the system')
def step_given_valid_ticket(context):
    # Create a valid ticket in the database dynamically
    context.ticket = Ticket.objects.create(
        train_name="Test Train",
        travel_date="2025-01-05",
        source="Station A",
        destination="Station B",
        departure=time(10, 0),  # Use datetime.time for valid time format
        class_type="Economy",
        fare=100
    )

@given('I do not have a valid ticket in the system')
def step_given_invalid_ticket(context):
    # Ensure no valid ticket exists in the database for the test
    context.ticket = None

@when('I verify the ticket using its details')
def step_when_verify_ticket_valid(context):
    if context.ticket:
        # Simulate GET request to verify the valid ticket
        context.response = client.get('/verify_ticket', {
            'train': context.ticket.train_name,
            'date': context.ticket.travel_date,
            'tid': context.ticket.id
        })
    else:
        # Simulate GET request with invalid ticket details
        context.response = client.get('/verify_ticket', {
            'train': "Invalid Train",
            'date': "2025-01-05",
            'tid': 999  # Non-existent ticket ID
        })

@when('I attempt to verify a ticket with invalid details')
def step_when_verify_ticket_invalid(context):
    # Store the invalid ticket details in the context
    context.train_name = "Invalid Train"
    context.travel_date = "2025-01-05"
    context.ticket_id = 999

    # Simulate GET request with invalid ticket details
    context.response = client.get('/verify_ticket', {
        'train': context.train_name,
        'date': context.travel_date,
        'tid': context.ticket_id
    })

@then('I see the ticket\'s validity confirmed with its details displayed')
def step_then_ticket_validity_confirmed(context):
    # Decode the response content
    response_content = context.response.content.decode()

    # Check if the response contains the success message and ticket details
    assert context.response.status_code == 200
    assert "This ticket is verified." in response_content, "Success message not found in response"
    assert f"Train Name: {context.ticket.train_name}" in response_content, "Train name not displayed correctly"
    assert f"Travel Date: {context.ticket.travel_date}" in response_content, "Travel date not displayed correctly"
    assert f"Ticket ID: {context.ticket.id}" in response_content, "Ticket ID not displayed correctly"

@then('I see an error message indicating the ticket is invalid')
def step_then_error_message(context):
    # Decode the response content
    response_content = context.response.content.decode()

    # Debug: Print the response content for troubleshooting
    # print(response_content)

    # Use the parameters stored in the context during the @when step
    train_name = context.train_name
    travel_date = context.travel_date
    ticket_id = context.ticket_id

    # Check if the response contains the error message and the requested details
    assert context.response.status_code == 200
    assert "This ticket is not verified." in response_content, "Error message not found in response"
    assert f"Train Name: {train_name}" in response_content, "Train name not displayed correctly"
    assert f"Travel Date: {travel_date}" in response_content, "Travel date not displayed correctly"
    assert f"Ticket ID: {ticket_id}" in response_content, "Ticket ID not displayed correctly"
