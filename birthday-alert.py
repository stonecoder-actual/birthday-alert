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
CSV_FILE_PATH = "rolladex.csv"

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

# Function to fetch a random quote from the Stoicism Quote API
def fetch_random_quote():
    """
    Fetches a random quote from the Stoicism Quote API.

    Returns:
        dict: The JSON response containing the quote if successful.
        None: If the request fails or encounters an error.
    """
    # Define the URL for the API endpoint
    url = "https://stoic-quotes.com/api/quote"

    try:
        # Make the GET request
        response = requests.get(url)

        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON response
            print(response.json())
            send_slack_message(f"Stoic QOTD: {response.json().get('text')} - {response.json().get('author')}")
            return
        else:
            print(f"Failed to retrieve quote. HTTP Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return None
    
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
        fetch_random_quote()
    except Exception as e:
        print(f"Error: {e}")