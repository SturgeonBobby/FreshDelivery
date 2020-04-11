# Description
This package automatically detects available delivery windows for Amazon Fresh orders and notifies you via email.

# How to use
1. Add items you wish to purchase to your Amazon shopping cart. This tool will not work properly if you have an empty cart
1. Download the appropriate web driver for your browser (e.g., the driver for Chrome can be downloaded [here](https://chromedriver.chromium.org)), and add it to the `PATH` environment variable
1. Clone this repo
1. Fill out the information in `keys.json`
    - `amazon_email`: Amazon email address
    - `amazon_pw`: Amazon password
    - `from_email`: Sender address of email notification when new delivery windows become available. Only Gmail and Outlook are supported at this time
    - `from_password`: Password of sender email
    - `to_emails`: Recipient address for the notification. Can be a list of emails
    - `to_errorfix`: Recipient address for when the code didn't run properly
1. From the top level of the repo, run `python fresh.py`
1. The program will keep running indefinitely, scanning your shopping cart at random intervals ranging from 10, 15, 20, 25, to 30 mins until interrupted by the keyboard (Control-C). You'll receive an email notification if there is an available delivery windows; if the code ran into an error, you'll receive the full trackback via email
