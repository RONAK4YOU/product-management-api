Feature: Product catalog management
  As a catalog user
  I want to create, retrieve, update, delete, and search products
  So that I can manage the product catalog

  Background:
    Given I am on the Home Page
    And the product catalog contains
      | name         | description              | price   | available | category    |
      | Laptop Pro   | Professional laptop      | 1299.99 | true      | Electronics |
      | Desk Lamp    | Adjustable desk lamp     | 34.50   | true      | Home        |
      | Headphones   | Noise-canceling headphones | 199.00  | false     | Electronics |
      | Coffee Maker | Automatic coffee maker   | 79.99   | true      | Kitchen     |

  Scenario: Read a product by name and retrieve its ID
    When I search for product "Laptop Pro"
    And I copy the product ID from the search results
    And I paste the copied ID into the product ID field
    And I click the "Retrieve" button
    Then I should see the message "Success"
    And the displayed product details include "Laptop Pro", "Professional laptop", "true", "Electronics", and "1299.99"

  Scenario: Update a product name
    When I search for product "Laptop Pro"
    And I copy the product ID from the search results
    And I change the product name to "Laptop Air"
    And I click the "Update" button
    Then I should see the message "Product updated"
    When I paste the copied ID into the product ID field
    And I click the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Laptop Air" in the results
    When I search for product "Laptop Air"
    Then I should see "Laptop Air" in the results
    And I should not see "Laptop Pro" in the results

  Scenario: Delete a product
    When I search for product "Desk Lamp"
    And I copy the product ID from the search results
    And I paste the copied ID into the product ID field
    And I click the "Delete" button
    Then I should see the message "Product deleted"
    When I search for product "Desk Lamp"
    Then I should not see "Desk Lamp" in the results

  Scenario: List all products
    When I click the "Clear" button
    And I click the "Search" button
    Then I should see the message "Success"
    And I should see "Laptop Pro" in the results
    And I should see "Desk Lamp" in the results

  Scenario: Search products by category
    When I click the "Clear" button
    And I select the "Electronics" category
    And I click the "Search" button
    Then I should see the message "Success"
    And I should see "Laptop Pro" in the results
    And I should not see "Desk Lamp" in the results

  Scenario: Search products by availability
    When I click the "Clear" button
    And I select "false" from the Available dropdown
    And I click the "Search" button
    Then I should see the message "Success"
    And I should see "Headphones" in the results
    And I should not see "Laptop Pro" in the results

  Scenario: Search products by name
    When I visit the Home Page
    And I click the "Clear" button
    And I enter "Laptop Pro" in the Product Name field
    And I click the "Search" button
    Then I should see the message "Success"
    And the displayed product has name "Laptop Pro" and description "Professional laptop"
