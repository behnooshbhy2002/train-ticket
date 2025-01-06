Feature: Cancel a booking

  As a user
  I want to cancel a booking
  So that I can free up the reserved seats

  Scenario: Cancel a booking successfully
    Given I have a confirmed booking
    When I cancel the booking
    Then the booking should be cancelled
    And booking shouldn't show in my booking history anymore
