import csv
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Slack webhook URL retrieved from environment variables
SLACK_WEBHOOK_URL = os.getenv("PERSONAL_SLACK_WEBHOOK_URL")
if not SLACK_WEBHOOK_URL:
    raise Exception("PERSONAL_SLACK_WEBHOOK_URL is not set in the .env file")

# Path to the CSV file containing birthdays
CSV_FILE_PATH = "birthdays.csv"

# Function to send a Slack message
def send_slack_message(message):
    """
    Sends a message to Slack using the webhook URL.
    Args:
        message (str): The message to send.
    Raises:
        Exception: If the Slack API call fails.
    """
    payload = {
        "text": message
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to send message to Slack: {response.status_code}, {response.text}")

# Function to check birthdays and send alerts
def check_birthdays():
    """
    Reads the CSV file, checks for birthdays matching today's date,
    and sends Slack alerts for matches.
    """
    today = datetime.now().strftime("%m/%d")
    print(today)
    with open(CSV_FILE_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_name = row.get('First Name', '').strip()
            last_name = row.get('Last Name', '').strip()
            dob = row.get('DOB', '').strip()
            print(first_name,last_name,dob)

            # Skip rows with missing or invalid DOB
            if not dob:
                print(f"Skipping row due to missing DOB: {row}")
                continue

            try:
                # Extract month and day from DOB (format: MM/DD/YYYY)
                dob_month_day = datetime.strptime(dob, "%m/%d/%Y").strftime("%m/%d")
                if dob_month_day == today:
                    send_slack_message(f"🎉 Happy Birthday, {first_name} {last_name}! 🎂")
            except ValueError:
                print(f"Skipping row due to invalid DOB format: {row}")
                continue

# Main execution
if __name__ == "__main__":
    try:
        check_birthdays()
    except Exception as e:
        print(f"Error: {e}")