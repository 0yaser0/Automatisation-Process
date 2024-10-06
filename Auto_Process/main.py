from AutoLogin.TikTokLoginAutomation import TikTokLoginAutomation
from EmailCreator.EmailCreator import EmailAutomation

if __name__ == "__main__":
    email_automation = EmailAutomation()
    email, password = email_automation.run()
    tiktok_login = TikTokLoginAutomation(email, password)
    tiktok_login.login()
