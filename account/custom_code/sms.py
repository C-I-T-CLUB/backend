from twilio.rest import Client
account_sid = "AC7556402d5007a362d36ef2d3ca62be9a"
auth_token = "29ceea204474f5901dc7ff5920a1bf32"

# verify
verification = Client(account_sid,auth_token)
twilio_number = "+12403926474"

# send message
def sendsms(phone,message):
    verification.messages.create(from_=twilio_number, to=f"+254{phone}",body=message)

# sendsms(798355947 , "HELLO AM TESTING CODE")
# print("send well...!..")