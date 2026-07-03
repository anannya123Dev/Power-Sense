# alert.py
import smtplib

def send_alert(power_value):
    sender = "your@gmail.com"
    receiver = "your@gmail.com"
    msg = f"Subject: ⚡ High Power Alert!\n\nPower consumption is HIGH: {power_value}W"
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login("your@gmail.com", "your_app_password")
        s.sendmail(sender, receiver, msg)