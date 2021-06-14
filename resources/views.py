import datetime
import jwt
from account.models import User
from .models import Resource
from account.custom_code import (authentication, password_hasher,string_generator, validator)
from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from citclub import settings
from .serializer import  FileSerializer

# Create your views here.
@api_view(['GET'])
def index_page(request):
    return_data = {
        "error" : "0",
        "message" : "Successful!.. Welcome to CIT CLUB Resoruces ENDPOINT"
    }
    return Response(return_data)



# post files
@api_view(["POST"])
@authentication.token_required
def upload_resource(request , DecriptionToken):
    try:
        file = request.data.get('file',None)
        course = request.data.get('course',None)
        unitname = request.data.get('unit_name',None)
        year = request.data.get('year',None)
        field = [file,course,year , unitname]
        if not None in field and not "" in field:
        	#get the user
        	user_data = User.objects.get(user_id=DecriptionToken["user_id"])
        	#get fileid
        	fileId = string_generator.alphanumeric(24)

        	#save the data
        	file_data = Resource(file_id =fileId , file = file , unitname = unitname , 
        		year = year , user =user_data , course = course )
        	file_data.save()
        	return_data = {
                "error": "0",
                "message": "File Uploaded Successful..!",
                "fileid":f"{file_data.file_id}",
                "course":f"{file_data.course}"
            }
        else:
        	return_data = {
                "error": "2",
                "message": "Invalid Parameters"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": "An error occured"
        }
        print(f"\n\n\n{return_data}\n\n\n")
    return Response(return_data)



# get all files
@api_view(["GET"])
def Files(request):
    try:
        files = Resource.objects.all().order_by('-file_id')
        serializer = FileSerializer(files , many =True)
        return_data ={
            "error":"0",
            "message":"Successful Retrived files",
            "data":serializer.data,
        }     
    except Exception as e:
        return_data={
            "error":"3",
            "errorIfor":f"{e}",
            "message":"An error Occured",
        }
    return Response(return_data)

# get file by id
@api_view(['GET'])
def FileDetails(request, fileid):
    tasks = Resource.objects.get(file_id=fileid)
    serializer = FileSerializer(tasks, many=False)
    return_data ={
        "error":"0",
        "message":"Successful Identified",
        "data":serializer.data
    }
    return Response(return_data)


from django.views.decorators.csrf import csrf_exempt
import jwt
from citclub import settings
# update file
@csrf_exempt
# @authentication.token_required
@api_view(['POST', "PATCH"])
def FileUpdate(request,fileid,DecriptionToken):
    try:
        DecriptionToken = jwt.decode(DecriptionToken,settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(user_id = DecriptionToken['user_id'])
        print(f"\n\n\n{Resource.objects.filter(file_id=fileid , user = user).exists()}\n\n")
        if Resource.objects.filter(file_id=fileid , user = user).exists():
            file_update = Resource.objects.get(file_id=fileid , user=user)
            serializer = FileSerializer(instance=file_update, data=request.data , partial = True)
            if serializer.is_valid():
                serializer.save()
                return_data ={
                    "error":"0",
                    "message":"Successful Updated",
                    "data":serializer.data
                }
            else:
                return_data ={
                    "error":f"3",
                    "message":"An Error Occured"
                }
        else:
            return_data ={
                "error":f"3",
                "message":"Not Authorised to update the resources"
            }
    except Exception as e:
        return_data ={
            "error":f"3  {e}",
            "message":"An Error Occured"
        }
    return Response(return_data)







