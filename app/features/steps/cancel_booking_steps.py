from behave import given, when, then
from django.contrib.auth import get_user_model
from app.models import Booking, Ticket
from django.test.client import Client
import uuid
from datetime import time  # Import for handling time fields

# Get the custom user model
CustomUser = get_user_model()

@given("I have a confirmed booking")
def step_given_confirmed_booking(context):
    # Create a test user with a unique username and email, and log them in
    context.client = Client()
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"  # Generate a unique username
    unique_email = f"{unique_username}@example.com"  # Generate a unique email based on the username
    context.user = CustomUser.objects.create_user(
        username=unique_username,
        password="testpassword",
        email=unique_email
    )
    context.client.login(username=unique_username, password="testpassword")
    
    # Create a confirmed booking for the user
    context.booking = Booking.objects.create(user=context.user, travel_date="2025-01-10")
    context.ticket = Ticket.objects.create(
        booking=context.booking,
        user=context.user,
        train_name="Test Train",
        source="Station A",
        destination="Station B",
        travel_date="2025-01-10",
        departure=time(10, 0),  # Use datetime.time for valid time format
        class_type="Economy",
        fare=100
    )

@when("I cancel the booking")
def step_when_cancel_booking(context):
    # Send a POST request to cancel the booking with a simulated referer
    context.response = context.client.post(
        "/cancel_booking", 
        {"booking_id": context.booking.id},
        HTTP_REFERER="/dashboard/"  # Simulating a referring page to avoid KeyError
    )

@then("the booking should be cancelled")
def step_then_booking_cancelled(context):
    # Check that the booking no longer exists
    assert not Booking.objects.filter(id=context.booking.id).exists()

@then("booking shouldn't show in my booking history anymore")
def step_then_booking_not_in_history(context):
    # Check that the booking is not in the user's booking history
    response = context.client.get("/booking_history")
    assert str(context.booking.id) not in response.content.decode()
