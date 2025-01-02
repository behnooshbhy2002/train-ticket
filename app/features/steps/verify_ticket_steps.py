from behave import given, when, then

class Ticket:
    def __init__(self, status, details=None):
        self.status = status
        self.details = details or {}

    def verify(self):
        if self.status == "Valid":
            return {"status": "Valid", "details": self.details}
        else:
            raise ValueError("Invalid Ticket")


@given('I have successfully obtained a ticket')
def step_given_valid_ticket(context):
    """Step for obtaining a valid ticket."""
    context.ticket = Ticket(status="Valid", details={"id": 123, "event": "Concert"})

@given('I have obtained a ticket with an invalid status')
def step_given_invalid_ticket(context):
    """Step for obtaining an invalid ticket."""
    context.ticket = Ticket(status="Invalid")

@when('I verify the ticket')
def step_when_verify_ticket(context):
    """Step for verifying a ticket."""
    try:
        context.verification_result = context.ticket.verify()
    except ValueError as e:
        context.verification_error = str(e)

@then('the ticket status should be "Valid"')
def step_then_ticket_status_valid(context):
    """Check that the ticket status is valid."""
    assert context.verification_result["status"] == "Valid", "Expected ticket status to be 'Valid'"

@then('the ticket details should be displayed correctly')
def step_then_ticket_details_correct(context):
    """Check that the ticket details are correct."""
    expected_details = {"id": 123, "event": "Concert"}
    assert context.verification_result["details"] == expected_details, "Ticket details do not match"

@then('an error message should be displayed indicating the ticket is invalid')
def step_then_ticket_invalid_error(context):
    """Check that an error message is displayed for an invalid ticket."""
    assert context.verification_error == "Invalid Ticket", "Expected error message: 'Invalid Ticket'"