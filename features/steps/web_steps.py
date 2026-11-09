"""Selenium browser steps for the product catalog UI."""
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select


def wait_for(context, by, selector):
    return WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((by, selector))
    )


@given("I am on the Home Page")
def step_home_page(context):
    context.driver.get(context.base_url)


@when("I visit the Home Page")
def step_visit_home_page(context):
    context.driver.get(context.base_url)


@when('I click the "{button}" button')
def step_button_click(context, button):
    element = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space()='{button}']"))
    )
    element.click()


@when('I search for product "{name}"')
def step_search_name(context, name):
    wait_for(context, By.ID, "search_name").clear()
    context.driver.find_element(By.ID, "search_name").send_keys(name)
    context.driver.find_element(By.ID, "search_button").click()


@when('I select the "{category}" category')
def step_select_category(context, category):
    field = wait_for(context, By.ID, "search_category")
    field.clear()
    field.send_keys(category)


@when('I select "{available}" from the Available dropdown')
def step_select_availability(context, available):
    Select(wait_for(context, By.ID, "search_available")).select_by_value(available.lower())


@when('I enter "{name}" in the Product Name field')
def step_enter_product_name(context, name):
    field = wait_for(context, By.ID, "search_name")
    field.clear()
    field.send_keys(name)


@when("I copy the product ID from the search results")
def step_copy_product_id(context):
    id_element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#search_results code"))
    )
    context.copied_product_id = id_element.text.strip()


@when("I paste the copied ID into the product ID field")
def step_paste_product_id(context):
    field = wait_for(context, By.ID, "product_id")
    field.clear()
    field.send_keys(context.copied_product_id)


@when('I change the product name to "{name}"')
def step_change_name(context, name):
    field = wait_for(context, By.ID, "name")
    field.clear()
    field.send_keys(name)


@then('I should see "{text}" in the results')
def step_text_present(context, text):
    results = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )
    assert text in results.text, f"Expected {text!r} in results: {results.text!r}"


@then('I should not see "{name}" in the results')
def step_text_absent(context, name):
    results = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )
    assert name not in results.text, f"Did not expect {name!r} in results: {results.text!r}"


@then('I should see the message "{message}"')
def step_message_present(context, message):
    flash = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "flash_message"))
    )
    assert message in flash.text, f"Expected message {message!r}; got {flash.text!r}"


@then('the displayed product has name "{name}" and description "{description}"')
def step_product_details(context, name, description):
    details = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "product_details"))
    )
    assert name in details.text
    assert description in details.text


@then('the displayed product details include "{name}", "{description}", "{available}", "{category}", and "{price}"')
def step_all_product_details(context, name, description, available, category, price):
    details = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "product_details"))
    )
    for value in (name, description, available, category, price):
        assert value in details.text, f"Expected {value!r} in product details: {details.text!r}"
