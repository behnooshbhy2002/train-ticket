Feature: Submit Feedback
  Description: As a user, I want to submit feedback about the system or my experience so that I can share my opinion.

  Scenario: Submitting Feedback Successfully
    Given the user is logged in
    And the user is on the feedback submission page
    When the user submits valid feedback
    Then the feedback is successfully submitted
    And a confirmation message is displayed

  Scenario: Submitting Invalid Feedback
    Given the user is logged in
    And the user is on the feedback submission page
    When the user submits invalid feedback
    Then the system displays an error message indicating the invalid feedback

  Scenario: Submitting Feedback Without Logging In
    Given the user is not logged in
    When the user tries to access the feedback submission page
    Then the user sees an error message indicating they need to log in
