Feature: Verify Ticket

Scenario: Successful Ticket Verification
    Given I have successfully obtained a ticket
    When I verify the ticket
    Then the ticket status should be "Valid"
    And the ticket details should be displayed correctly

  Scenario: Failed Ticket Verification
    Given I have obtained a ticket with an invalid status
    When I verify the ticket
    Then an error message should be displayed indicating the ticket is invalid