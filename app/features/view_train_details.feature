Feature: View Train Details
  As a user
  I want to view train details such as departure time, arrival time, and class type
  So that I can make an informed decision

  Scenario: View Train Details Successfully
    Given the user is logged in to the system
    And the user selects a train
    When the user views the train details
    Then the user sees the departure time, arrival time, and class type of the train

  Scenario: Invalid Train Selection
    Given the user is logged in to the system
    And the user selects a non-existent train
    When the user views the train details
    Then the system displays an error message indicating that the train does not exist

  Scenario: No Train Selected
    Given the user is logged in to the system
    And the user has not selected a train
    When the user views the train details
    Then the system displays a message indicating that no train is selected
