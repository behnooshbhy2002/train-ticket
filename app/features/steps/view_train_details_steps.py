from behave import given, when, then
from django.contrib.auth.models import User
from app.models import Train, ClassType, Booking, BookingDetail, Station
from django.test import Client
from datetime import datetime, time
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.utils.dateformat import format


@given(u'a user is logged in')
def step_impl(context):
    User = get_user_model()
    context.user, created = User.objects.get_or_create(
        username="testuser",
        defaults={"email": "testuser@example.com", "password": "password123"},
    )
    if not created:
        context.user.set_password("password123")
        context.user.save()

    # Initialize the Django test client
    context.client = Client()
    context.client.login(username="testuser", password="password123")


@given("the user has booked at least one train")
def step_impl(context):
    # Ensure uniqueness or handle duplicates for source station
    source_stations = Station.objects.filter(name="Station A")
    if source_stations.exists():
        source_station = source_stations.first()
    else:
        source_station = Station.objects.create(name="Station A")

    # Ensure uniqueness or handle duplicates for destination station
    destination_stations = Station.objects.filter(name="Station B")
    if destination_stations.exists():
        destination_station = destination_stations.first()
    else:
        destination_station = Station.objects.create(name="Station B")

    # Create a test train
    train = Train.objects.create(name="Test Train", source=source_station, destination=destination_station)

    # Create a class type
    class_type, _ = ClassType.objects.get_or_create(name="First Class")

    # Create a booking
    booking = Booking.objects.create(user=context.user, travel_date=now())

    # Create a booking detail
    BookingDetail.objects.create(
        booking=booking,
        train=train,
        source=source_station,
        destination=destination_station,
        travel_date=booking.travel_date,
        nop=1,
        adult=1,
        child=0,
        class_type=class_type.name,
        fpp=100,
        total_fare=100,
        travel_time=time(hour=10, minute=0),
        travel_dt=now(),
    )


@when("the user navigates to the booking history page")
def step_impl(context):
    # Simulate navigating to the booking history page
    context.response = context.client.get("/booking_history")  # Replace with the actual URL for booking history
    
    # Assert the page loaded successfully
    assert context.response.status_code == 200, "Failed to load the booking history page."
    assert "Your Bookings" in context.response.content.decode(), "The booking history page content is not as expected."


from bs4 import BeautifulSoup

@then("the user should see a list of bookings")
def step_impl(context):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(context.response.content, "html.parser")

    # Find all rows in the bookings table
    rows = soup.find_all("tr", class_="text-center")

    # Assert that there are rows in the table
    assert len(rows) > 0, "No bookings found in the booking history table."

    # Debug: Print the booking details (optional)
    for row in rows:
        columns = row.find_all("td")
        if columns:
            booking_id = row.find("th").text.strip()
            booking_date = columns[0].text.strip()
            booking_time = columns[1].text.strip()
            booking_status = columns[2].text.strip()
            # print(f"Booking ID: {booking_id}, Date: {booking_date}, Time: {booking_time}, Status: {booking_status}")

    # Optionally, verify specific booking details (e.g., a specific booking ID exists)
    booking_ids = [row.find("th").text.strip() for row in rows]
    assert "135" in booking_ids, "Booking ID 135 is not found in the booking history."   


@then("each booking should display the departure time, arrival time, and class type.")
def step_impl(context):
    assert context.response is not None, "Response is None. Ensure the test is setting context.response."

    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(context.response.content, "html.parser")

    # Find the table body containing the bookings
    tbody = soup.select_one("table.table tbody")
    assert tbody is not None, "Booking table is missing in the HTML response."

    # Find all rows in the table body
    booking_rows = tbody.select("tr")
    assert len(booking_rows) > 0, "No bookings found in the booking table."

    for row in booking_rows:
        # Validate the structure of each row
        cells = row.select("td, th")
        assert len(cells) >= 6, f"Booking row does not have all required columns: {len(cells)} found."

        # Extract values from mandatory columns
        booking_id = cells[0].text.strip()
        booking_date = cells[1].text.strip()
        booking_time = cells[2].text.strip()
        booking_status = cells[3].text.strip()
        view_details_button = cells[4].select_one("a[href*='booking_history/booking_detail/']")
        get_ticket_button = cells[5].select_one("a[href*='booking_history/ticket/']")

        # Assertions for mandatory columns
        assert booking_id.isdigit(), f"Invalid Booking ID: {booking_id}"
        assert booking_date, "Booking Date is missing or empty."
        assert booking_time, "Booking Time is missing or empty."
        assert booking_status, "Booking Status is missing or empty."
        assert view_details_button is not None, "View Details button is missing."
        assert "View Details" in view_details_button.text.strip(), f"Incorrect text in View Details button: {view_details_button.text.strip()}"
        assert get_ticket_button is not None, "Get Ticket button is missing."
        assert "Get Ticket" in get_ticket_button.text.strip(), f"Incorrect text in Get Ticket button: {get_ticket_button.text.strip()}"

        # Optional: Validate the Cancel Booking column (if present)
        if len(cells) == 7:  # Only check if the column exists
            cancel_booking_form = cells[6].select_one("form[action='cancel_booking']")
            if cancel_booking_form:
                cancel_button = cancel_booking_form.select_one("button[type='submit']")
                assert cancel_button is not None, "Cancel Booking button is missing in the form."
                assert "Cancel Booking" in cancel_button.text.strip(), f"Incorrect text in Cancel Booking button: {cancel_button.text.strip()}"