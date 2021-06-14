import datetime

import jwt
from account.models import User
from account.custom_code import (authentication, password_hasher,
                        string_generator, validator)
from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from citclub import settings


# Create your views here.
@api_view(['GET'])
def index_page(request):
    return_data = {
        "error" : "0",
        "message" : "Successful!.. Welcome to CIT CLUB ACCOUNT ENDPOINT"
    }
    return Response(return_data)



@api_view(["POST"])
def user_registration(request):
    try:
        firstName = request.data.get('firstname',None)
        lastName = request.data.get('lastname',None)
        phoneNumber = request.data.get('phonenumber',None)
        email = request.data.get('email',None)
        gender = request.data.get('gender',None)
        password = request.data.get('password',None)
        reg_field = [firstName,lastName,phoneNumber,email,password , gender]
        #print([reg_field])
        # print(request.data)
        if not None in reg_field and not "" in reg_field:
            if  User.objects.filter(user_phone =phoneNumber).exists() or  User.objects.filter(email =email).exists():
                return_data = {
                    "error": "1",
                    "message": "User Exists",
                    # "user":User.objects.filter(email =email)[0].email,
                    # "pass":User.objects.filter(email =email)[0].user_password
                }
                # or validator.checkphone(phoneNumber)== False
            elif validator.checkmail(email) == False :
                return_data = {
                    "error": "1",
                    "message": "Email or Phone number is Invalid"
                }
            else:
                #generate user_id
                userRandomId = string_generator.alphanumeric(20)
                #encrypt password
                encryped_password = password_hasher.generate_password_hash(password)
                #Save user_data
                new_userData = User(user_id=userRandomId,firstname=firstName,lastname=lastName,
                                email=email,user_phone=phoneNumber,user_gender=gender,
                                user_password=encryped_password,)
                new_userData.save()
                #get user role
                role = User.objects.get(user_id=userRandomId).role
                #Generate token
                timeLimit= datetime.datetime.now() + datetime.timedelta(minutes=1440) #set duration for token
                payload = {"user_id": f"{userRandomId}",
                           "role": role,
                           "exp":timeLimit}
                token = jwt.encode(payload,settings.SECRET_KEY)
                message = f"Welcome to CIT CLUB, your verification code is {payload}"
                # sms.sendsms(phoneNumber[1:],message)
                print(f"""
                {message}
                """)
                return_data = {
                    "error": "0",
                    "message": "The registration was successful,you can now login",
                    "token": f"{token.decode('UTF-8')}",
                    "elapsed_time": f"{timeLimit}",
                    }
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Parrameter"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": f"An error occured    {e}"
        }
    return Response(return_data)

#User login
@api_view(["POST"])
def user_login(request):
    try:
        email_phone = request.data.get("email_phone",None)
        password = request.data.get("password",None)
        field = [email_phone,password]
        if not None in field and not '' in field:
            validate_mail = validator.checkmail(email_phone)
            # validate_phone = validator.checkphone(email_phone)
            validate_phone = True
            if validate_mail == True:
                if User.objects.filter(email =email_phone).exists() == False:
                    return_data = {
                        "error": "1",
                        "message": "User does not exist"
                    }
                else:
                    user_data = User.objects.get(email=email_phone)
                    is_valid_password = password_hasher.check_password_match(password,user_data.user_password)
                    #Generate token
                    timeLimit= datetime.datetime.now() + datetime.timedelta(minutes=1440) #set limit for user
                    payload = {"user_id": f'{user_data.user_id}',
                               "role": user_data.role,
                               "exp":timeLimit}
                    token = jwt.encode(payload,settings.SECRET_KEY)
                    if is_valid_password:
                        return_data = {
                            "error": "0",
                            "message": "Successfull",
                            "token": token.decode('UTF-8'),
                            "token-expiration": f"{timeLimit}",
                            "user_details": [
                                {
                                    "firstname": f"{user_data.firstname}",
                                    "lastname": f"{user_data.lastname}",
                                    "email": f"{user_data.email}",
                                    "phone_number": f"{user_data.user_phone}",
                                    "gender": f"{user_data.user_gender}",
                                 
                                }
                            ]

                        }
                    else:
                        return_data = {
                            "error" : "1",
                            "message" : "Wrong Password"
                        }
            elif validate_phone == True:
                if User.objects.filter(user_phone =email_phone).exists() == False:
                    return_data = {
                        "error": "1",
                        "message": "User does not exist"
                    }
                else:
                    user_data = User.objects.get(user_phone=email_phone)
                    is_valid_password = password_hasher.check_password_match(password,user_data.user_password)
                    #Generate token
                    timeLimit= datetime.datetime.now() + datetime.timedelta(minutes=1440) #set limit for user
                    payload = {"user_id": f'{user_data.user_id}',
                               "role": user_data.role,
                               "exp":timeLimit}
                    token = jwt.encode(payload,settings.SECRET_KEY)
                    if is_valid_password:
                        return_data = {
                            "error": "0",
                            "message": "Successfull",
                            "token": token.decode('UTF-8'),
                            "token-expiration": f"{timeLimit}",
                            "user_details": [
                                {
                                    "firstname": f"{user_data.firstname}",
                                    "lastname": f"{user_data.lastname}",
                                    "email": f"{user_data.email}",
                                    "phone_number": f"{user_data.user_phone}",
                                    "gender": f"{user_data.user_gender}",
                                }
                            ]

                        }
                    else:
                        return_data = {
                            "error" : "1",
                            "message" : "Wrong Password"
                        }
            else:
                return_data = {
                    "error": "2",
                    "message": "Email or Phone Number is Invalid"
                }
        else:
            return_data = {
                "error" : "2",
                "message" : "Invalid Parameters"
                }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": f"An error occured      {e}"
        }
    return Response(return_data)




# #Change password
@api_view(["POST"])
@authentication.token_required
def password_change(request,decrypedToken):
    try:
        new_password = request.data.get("new_password",None)
        old_password = request.data.get("old_password",None)
        fields = [old_password , new_password]
        if not None in fields and not "" in fields:
            #get user info
            user_data = User.objects.get(user_id=decrypedToken["user_id"])
            is_valid_password = password_hasher.check_password_match(old_password,user_data.user_password)
            if is_valid_password:
                #encrypt password
                encryptpassword = password_hasher.generate_password_hash(new_password)
                user_data.user_password = encryptpassword
                user_data.save()
                return_data = {
                    "error": "0",
                    "message": "Successfull, Password Changed"
                }
            else:
                return_data = {
                    "error": "1",
                    "message": "Wrong Old password Please recheck again!"
                }
        else:
            return_data = {
                "error": "2",
                "message": "Invalid Parameters"
            }
    except Exception:
        return_data = {
            "error": "3",
            "message": "An error occured"
        }
    return Response(return_data)


@api_view(["GET"])
@authentication.token_required
def user_profile(request,decrypedToken):
    try:
        userID = decrypedToken['user_id']
        UserInfo = User.objects.get(user_id=userID)
        if decrypedToken['role'] == 'user':
            UserInfo = User.objects.get(user_id=userID)
            return_data = {
                "error": "0",
                "message": "Successfull",
                "data": {
                    "user_details": {
                        "first_name": f"{UserInfo.firstname}",
                        "last_name": f"{UserInfo.lastname}",
                        "email": f"{UserInfo.email}",
                        "phone_number": f"{UserInfo.user_phone}",
                        "gender": f"{UserInfo.user_gender}",
                        "role": f"{UserInfo.role}"
                        }
                    ,
                    "user_uploads": {
                        "id": f"NULLS",
                        "uploads": f"NULLS",
                        "favourites": f"NULLS",
                        },
                    "student_infor": {"name":"NULLS"}

                    }
                }
        else:
            #if role isnot a normal user
            UserInfo = User.objects.get(user_id=userID)
            return_data = {
                "error": "0",
                "message": "Successfull",
                "data": {
                    "user_details": {
                    "first_name": f"{UserInfo.firstname}",
                    "last_name": f"{UserInfo.lastname}",
                    "email": f"{UserInfo.email}",
                    "phone_number": f"{UserInfo.user_phone}",
                    "gender": f"{UserInfo.user_gender}",
                    "role": f"{UserInfo.role}"
                    },
                    "USER_ROLE": f"CHAIR",
                    "DETAILS": "ORGANISER"

                    }
                }
    except Exception:
        return_data = {
            "error": "3",
            "message": "An error occured"
        }
    return Response(return_data)



@api_view(["POST"])
def password_reset_code(request):
    try:
        phone_number = request.data.get('phone_number',None)
        if phone_number != None and phone_number != "":
            if User.objects.filter(email =phone_number).exists() == False:
                return_data = {
                    "error": "1",
                    "message": "User does not exist"
                }
            else:
                user_data = User.objects.get(email=phone_number)
                generate_pin = string_generator.alphanumeric(15)
                user_data.password_reset_code = generate_pin
                user_data.save()
                message = f"Welcome to citclub, your password reset code is {generate_pin}"
                # send the code to email....
                print(f"""


                    {generate_pin}

                    """)

                # end of code send to the email
                timeLimit= datetime.datetime.now() + datetime.timedelta(minutes=1440) #set limit for user
                payload = {"user_id": f'{user_data.user_id}',
                           "role": user_data.role,
                           "exp":timeLimit}
                token = jwt.encode(payload,settings.SECRET_KEY)
                return_data = {
                    "error": "0",
                    "code" : "TESTING....server.com/?code=" + generate_pin,
                    "code" : generate_pin,
                    "message": "Successful, reset code sent to Phone Number/Email",
                    "token": token.decode('UTF-8')
                }
        else:
            return_data = {
                "error": "2",
                "message": "Invalid Parameter"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": f"An error occured as {e}"
        }
    return Response(return_data)



# token must be reset in order to use it
@api_view(["POST"])
@authentication.token_required
def forgoten_password_change(request,decrypedToken):
    try:
        reset_code = request.data.get("reset_code",None)
        new_password = request.data.get("new_password",None)
        fields = [reset_code,new_password]
        if not None in fields and not "" in fields:
            #get user info
            user_data = User.objects.get(user_id=decrypedToken["user_id"])
            otp_reset_code = otp.objects.get(user__user_id=decrypedToken["user_id"]).password_reset_code
            print(otp_reset_code)
            if reset_code == otp_reset_code:
                #encrypt password
                encryptpassword = password_functions.generate_password_hash(new_password)
                user_data.user_password = encryptpassword
                user_data.save()
                return_data = {
                    "error": "0",
                    "message": "Successfull, Password Changed"
                }
            elif reset_code != otp_reset_code:
                return_data = {
                    "error": "1",
                    "message": "Code does not Match"
                }
        else:
            return_data = {
                "error": "2",
                "message": "Invalid Parameters"
            }
    except Exception:
        return_data = {
            "error": "3",
            "message": "An error occured"
        }
    return Response(return_data)
