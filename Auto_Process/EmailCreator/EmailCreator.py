import requests
import time
import random
import string


# 1secmail API
def generate_temp_email():
    url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
    response = requests.get(url)
    email = response.json()[0]
    print(f"Temporary Email: {email}")
    return email


def extract_email_details(email):
    username, domain = email.split('@')
    return username, domain


def generate_password(length=12):
    if length < 4:
        raise ValueError("Password length should be at least 4 characters.")

    upper = random.choice(string.ascii_uppercase)
    lower = ''.join(random.choice(string.ascii_lowercase) for _ in range(length - 3))
    digit = random.choice(string.digits)
    special = random.choice('!@#$%^&*(),.?":{}|<>')

    password = upper + lower + digit + special
    password = ''.join(random.sample(password, len(password)))
    print(f"Generated Password: {password}")
    return password


def check_inbox(username, domain):
    inbox_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
    response = requests.get(inbox_url)
    return response.json()


def get_email_content(username, domain, message_id):
    message_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={message_id}"
    response = requests.get(message_url)
    return response.json()


def extract_verification_code(email_body):
    import re
    code = re.findall(r'\b\d{4,6}\b', email_body)
    if code:
        return code[0]
    return None


def main():
    # Generate temporary email and password
    email = generate_temp_email()
    password = generate_password()  # Create a secure password
    username, domain = extract_email_details(email)

    print("Waiting for the verification email...")
    verification_code = None
    while not verification_code:
        time.sleep(5)
        inbox = check_inbox(username, domain)
        if inbox:
            print("Email received!")
            message_id = inbox[0]['id']
            email_content = get_email_content(username, domain, message_id)
            print("Email content received:", email_content)

            verification_code = extract_verification_code(email_content['body'])
            if verification_code:
                print(f"Verification code found: {verification_code}")
                break
        else:
            print("No emails yet. Checking again...")


if __name__ == "__main__":
    main()
