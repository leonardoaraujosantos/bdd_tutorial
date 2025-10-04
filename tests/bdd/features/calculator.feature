Feature: Calculator
  As a user of the calculator API
  I want to perform simple operations
  So that I can get correct results

  Scenario: Add two numbers
    Given the calculator is running
    When I add 2 and 3
    Then the result should be 5

  Scenario: Subtract two numbers
    Given the calculator is running
    When I subtract 10 and 4
    Then the result should be 6

  Scenario: Multiply two numbers
    Given the calculator is running
    When I multiply 3 and 4
    Then the result should be 12

  Scenario: Divide two numbers
    Given the calculator is running
    When I divide 10 and 2
    Then the result should be 5

  Scenario: Add negative numbers
    Given the calculator is running
    When I add -5 and -3
    Then the result should be -8

  #Scenario: Divide by zero
  #  Given the calculator is running
  #  When I attempt to divide 10 by 0
  #  Then I should receive an error message
