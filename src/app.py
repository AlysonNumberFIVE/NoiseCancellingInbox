# Code is being added tentatively. I need to fix a bunch of security holes.

from flask import Flask, render_template
from gmail import gmail, summarise_text
from build_email import Object, unpack_data
from flask_mail import Mail, Message

from aws import upload_file_to_s3

import os

from datetime import datetime, timedelta
from test import email_test

app = Flask(__name__)
mail = Mail(app)

# Configure the mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


def the_week_of():
    """
    Ensure we're only ever looking at the week that passed.

    :return: A string showing the date of today and 7 days prior in the format
        [SEVEN_DAYS_AGO] - [TODAY], [MONTH(s)]
    """
    # Get today's date
    today = datetime.now()

    # Get the date 7 days ago
    seven_days_ago = today - timedelta(days=7)

    # Format the dates
    today_str = today.strftime('%d %b')
    seven_days_ago_str = seven_days_ago.strftime('%d %b')

    # Get the months
    month_today = today.strftime('%b')
    month_seven_days_ago = seven_days_ago.strftime('%b')

    # Format the month(s)
    if month_today == month_seven_days_ago:
        month_str = month_today
    else:
        month_str = month_seven_days_ago + "/" + month_today

    return f"{seven_days_ago_str} - {today_str}, {month_str}"


def send_mail(email_list, url):
    """
    Send the newsletter after mail's been summarized.
    :param: email_list: The list of email objects that contain
        the heading, summary, sender and date
    :param: url: The storage location of the email banner.
    """

    msg = Message("This Week's Noise In Your Inbox", 
        sender=os.environ.get("MAIL_USERNAME"), 
        recipients=os.environ.get("RECIPIENT_EMAIL"))
    
    msg.html = render_template('email.html',
        email_list=email_list,
        name=os.environ.get("RECIPIENT_NAME"),
        week_of=the_week_of(),
        logo=url
    )
    mail.send(msg)


def index():
    """
    Sends a weekly newsletter about what's going on in your inbox.
    """
    # Get all emails
    email_list = gmail()

    # GPT that shit
    email = summarise_text(email_list)

    # Prepare the banner
    url = upload_file_to_s3(
        os.environ.get("AWS_STORAGE_BUCKET")
    )
    
    # Extract that into the list of email summaries.
    email_objects = unpack_data(email)

    # Send the mail.
    send_mail(email_objects, url)


if __name__ == '__main__':
    index()
