Feature: View Train Details in Booking History

  As a user,
  I want to view train details that I booked in my booking history such as departure time, arrival time, and class type,
  So that I can make sure I booked the right train.

  Scenario: User views booking details in booking history
    Given a user is logged in
    And the user has booked at least one train
    When the user navigates to the booking history page
    Then the user should see a list of bookings
    And each booking should display the departure time, arrival time, and class type.
