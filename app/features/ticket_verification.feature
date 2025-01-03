Feature: Verify Ticket Validity
  As a user, I want to verify my ticket after I have obtained it,
  so that I can confirm its validity and ensure it is ready for use.

  Scenario: Valid Ticket Verification
    Given I have a valid ticket in the system
    When I verify the ticket using its details
    Then I see the ticket's validity confirmed with its details displayed

  Scenario: Invalid Ticket Verification
    Given I do not have a valid ticket in the system
    When I attempt to verify a ticket with invalid details
    Then I see an error message indicating the ticket is invalid
