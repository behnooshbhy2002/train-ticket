Feature: Cancel a booking

  As a user
  I want to cancel a booking if my plans change
  So that I can free up the reserved seats

  Scenario: Cancel a booking due to plan change
    Given I have made a booking for a specific event
    Given my plans have changed
    When I attempt to cancel the booking
    Then the booking should be cancelled and the seats should be freed up
