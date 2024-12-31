Feature: Search Form Validation
  As a user
  I want to be notified if I enter incomplete or incorrect information in the search form
  So that I can correct it

  Scenario: Search form with incomplete information
    Given the search form is displayed
    When I submit the form with incomplete information
    Then I should see error messages for the required fields

  Scenario: Search form with incorrect information
    Given the search form is displayed
    When I submit the form with incorrect information
    Then I should see error messages for the incorrect fields

  Scenario: Search form with valid information
    Given the search form is displayed
    When I submit the form with valid information
    Then I should be redirected to the available trains page