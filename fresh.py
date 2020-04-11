import json
import random
import smtplib
import time
import traceback
from collections import defaultdict
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver


with open("keys.json") as f:
    keys = json.loads(f.read())


def check_availability():
    url = "https://www.amazon.com"
    amazon_email = keys["amazon_email"]
    amazon_pw = keys["amazon_pw"]

    # Go to site
    options = webdriver.chrome.options.Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)

    try:
        # Click sign-in
        driver.implicitly_wait(5)
        sign_in = driver.find_element_by_id("nav-link-accountList")
        sign_in.click()
        time.sleep(3)

        # Enter email
        driver.implicitly_wait(5)
        email_field = driver.find_element_by_id("ap_email")
        email_field.click()
        email_field.send_keys(amazon_email)
        email_field.submit()
        time.sleep(3)

        # Enter password
        driver.implicitly_wait(5)
        pw_field = driver.find_element_by_id("ap_password")
        pw_field.click()
        pw_field.send_keys(amazon_pw)
        pw_field.submit()
        time.sleep(3)

        # Click shopping cart
        driver.implicitly_wait(5)
        cart = driver.find_element_by_id("nav-cart")
        cart.click()
        time.sleep(3)

        # Click collapsed item list
        item_list = driver.find_element_by_class_name("sc-carts-expand-link")
        item_list.click()

        # Examine availability of items in cart
        items_in_cart = driver.find_elements_by_class_name("sc-list-item-content")

        with open("categories.json") as f:
            item_categories = json.loads(f.read())

        available_items = defaultdict(list)

        for item in items_in_cart:
            item_name = item.find_element_by_class_name("sc-product-title").text.lower()
            item_quantity = item.find_element_by_class_name("a-button-text").text

            found_match = False
            for category, sample_items in item_categories.items():
                for sample_item in sample_items:
                    # Avoid potential misses due to spacing, e.g., "blueberry" vs. "blue berry"
                    if sample_item.replace(" ", "") in item_name.replace(" ", ""):
                        available_items[category].append((sample_item, item_quantity))
                        found_match = True
            if not found_match:
                available_items["other"].append((item_name, item_quantity))

        for category, available_items in available_items.items():
            print(category)
            for item, quantity in available_items:
                print(f"  - {item}, {quantity}")

        # Click checkout
        driver.implicitly_wait(5)
        checkout = driver.find_element_by_class_name("a-button-input")
        checkout.click()

        # Click continue
        driver.implicitly_wait(5)
        continue_button = driver.find_element_by_class_name("a-button-text")
        continue_button.click()
        time.sleep(3)

        # Get availabilities
        driver.implicitly_wait(5)
        slots = driver.find_elements_by_class_name("ufss-date-select-toggle-container")
        time.sleep(3)

        has_availability = parse_availability(slots)

    except:
        error_msg = traceback.format_exc()
        send_mail(error_msg, subject="Error", to_emails=keys["to_errorfix"])
        raise
    finally:
        driver.close()
    return has_availability


def parse_availability(slots):
    current_time = str(datetime.now())

    has_availability = any("Not available" not in slot.text for slot in slots)
    if has_availability:
        msg_to_send = "\n\n".join(slot.text for slot in slots)
        send_mail(msg_to_send)

    with open("availability_history.txt", "a") as f:
        line_to_append = f"\n{current_time},{has_availability}"
        f.write(line_to_append)

    print(line_to_append, end=" ")

    return has_availability


def send_mail(
    message,
    subject="Amazon availabilities",
    from_email=keys["from_email"],
    from_password=keys["from_password"],
    to_emails=keys["to_emails"],
):

    # Log in to email
    if "outlook" in from_email:
        server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        server.starttls()
        server.ehlo()
    else:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(from_email, from_password)

    # Compose email
    text_to_send = "Subject: {}\n\n{}".format(subject, message)

    # Send email
    server.sendmail(from_email, to_emails, text_to_send)
    server.quit()


def main():
    while True:
        time_to_wait = random.choice([10, 15, 20, 25, 30])
        check_availability()
        print(f"Will check again in {time_to_wait} mins.")
        time.sleep(60 * time_to_wait)


main()
