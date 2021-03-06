Feature: Managing groups

  Scenario: Creating group
     Given I am logged as Super user
      When I create new group
      Then Created group is visible on the list

  Scenario: Updating group
     Given I am logged as Super user
      When I create new group
       And I add permission "can add user"
       And I click "Save and continue editing" button
      Then I should see "can add user" in "Choosen permissions"

  Scenario: Deleting group
     Given I am logged as Super user
      When I create new group
       And I remove previously created group
      Then Group is not visible on the list