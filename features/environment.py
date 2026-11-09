import os
import requests
from selenium import webdriver


def before_all(context):
    context.base_url = os.getenv("PRODUCT_API_URL", "http://127.0.0.1:5000")
    options = webdriver.ChromeOptions()
    if os.getenv("BROWSER_HEADLESS", "true").lower() == "true":
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    context.driver = webdriver.Chrome(options=options)
    context.driver.set_window_size(1280, 900)


def before_scenario(context, scenario):
    # Keep scenarios independent by clearing test records through the API.
    response = requests.get(f"{context.base_url}/products", timeout=10)
    if response.ok:
        for product in response.json().get("products", []):
            requests.delete(f"{context.base_url}/products/{product['id']}", timeout=10)


def after_all(context):
    if getattr(context, "driver", None):
        context.driver.quit()
