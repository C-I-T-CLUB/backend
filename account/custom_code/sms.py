from twilio.rest import Client
from citclub import settings
account_sid = settings.SMS_SID
auth_token = settings.SMS_TOKEN

# verify
verification = Client(account_sid,auth_token)
twilio_number = "+12403926474"

# send message
def sendsms(phone,message):
    verification.messages.create(from_=twilio_number, to=f"+254{phone}",body=message)

sendsms(798355947 , "HELLO AM TESTING CODE")
# print("send well...!..")