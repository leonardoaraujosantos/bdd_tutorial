Feature: Bad Calculator (Passes BDD but has terrible implementation)
  As a demonstration of how BDD can pass with bad code
  I want to show that behavior can be correct while implementation is terrible
  So that developers understand BDD alone is not enough

  Background:
    Given the bad calculator is running

  Scenario: Bad calculator can add two numbers (but uses eval internally!)
    When I add 2 and 3 using bad calculator
    Then the bad calculator result should be 5
    # Note: This passes BDD but internally uses dangerous eval()!

  Scenario: Bad calculator can subtract (but uses exec internally!)
    When I subtract 10 and 4 using bad calculator
    Then the bad calculator result should be 6
    # Note: This passes BDD but uses exec() - major security issue!

  Scenario: Bad calculator can multiply (but uses shell injection!)
    When I multiply 3 and 4 using bad calculator
    Then the bad calculator result should be 12
    # Note: This passes BDD but uses subprocess with shell=True - vulnerable!

  Scenario: Bad calculator handles division
    When I divide 10 and 2 using bad calculator
    Then the bad calculator result should be 5
    # Note: Poor error handling but this scenario passes

  # This scenario shows the limitation of BDD
  # The behavior is correct, but the implementation is dangerously flawed!
