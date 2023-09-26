import smtplib
from email.message import EmailMessage
import ssl
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

sender_email = 'nicholasmendoza140@gmail.com'
sender_password = os.getenv("EMAIL_PASSWORD")
receiver_email = 'nikkomdoza@gmail.com'

api_key = os.getenv("API_KEY")
api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q=94533&aqi=no"

temperature = ''
condition = ''
response = requests.get(api_url)
if response.status_code == 200:
    data = json.loads(response.text)
    temperature = data['current']['temp_f']
    condition = data['current']['condition']['text']
else:
    print(f"Request failed: {response.status_code}")

subject = "Today's weather"
body = f"""
The weather today in Fairfield is {temperature}\u00b0F and {condition}.
"""

em = EmailMessage()
em['From'] = sender_email
em['To'] = receiver_email
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, em.as_string())
    server.quit()
except Exception as e:
    print(f"Error: {str(e)}")