import requests
import time
import random
import string
import re

class EmailAutomation:
    def __init__(self):
        self.email = None
        self.username = None
        self.domain = None
        self.verification_code = None

    def generate_temp_email(self):
        url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.email = response.json()[0]
            self.username, self.domain = self.extract_email_details(self.email)
            print(f"Temporary Email: {self.email}")
        except requests.exceptions.RequestException as e:
            print(f"Error generating temporary email: {e}")
        except (IndexError, ValueError) as e:
            print(f"Error processing email response: {e}")

    @staticmethod
    def extract_email_details(email):
        username, domain = email.split('@')
        return username, domain

    @staticmethod
    def generate_password(length=12):
        if length < 4:
            raise ValueError("Password length should be at least 4 characters.")

        upper = random.choice(string.ascii_uppercase)
        lower = ''.join(random.choice(string.ascii_lowercase) for _ in range(length - 3))
        digit = random.choice(string.digits)
        special = random.choice('(),.;')

        password = upper + lower + digit + special
        password = ''.join(random.sample(password, len(password)))
        print(f"Generated Password: {password}")
        return password

    def check_inbox(self):
        inbox_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={self.username}&domain={self.domain}"
        try:
            response = requests.get(inbox_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error checking inbox: {e}")
            return []

    def get_email_content(self, message_id):
        message_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={self.username}&domain={self.domain}&id={message_id}"
        try:
            response = requests.get(message_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting email content: {e}")
            return {}

    @staticmethod
    def extract_verification_code(email_body):
        code = re.findall(r'\b\d{4,6}\b', email_body)
        return code[0] if code else None

    def wait_for_verification_email(self):
        print("Waiting for the verification email...")
        while not self.verification_code:
            time.sleep(5)
            inbox = self.check_inbox()
            if inbox:
                print("Email received!")
                message_id = inbox[0]['id']
                email_content = self.get_email_content(message_id)
                if email_content:
                    print("Email content received:", email_content)
                    self.verification_code = self.extract_verification_code(email_content.get('body', ''))
                    if self.verification_code:
                        print(f"Verification code found: {self.verification_code}")
                        break
            else:
                print("No emails yet. Checking again...")

    def run(self):
        self.generate_temp_email()
        password = self.generate_password()
        #self.wait_for_verification_email()
        return self.email, password
