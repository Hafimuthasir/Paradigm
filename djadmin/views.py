from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from djapp.models import *
from djapp.serializer import *

# Create your views here.
@api_view(['POST'])
def logadmin(request):
    print('in logadmin')
    username = request.data['username']
    password = request.data['password']
    print(username,password)
    check = admins.objects.filter(user_name=username,password=password).first()
    if check :
        admincheck = 'True'
    else :
        admincheck = 'False'
    return Response(admincheck)


@api_view(['GET','POST'])
def userlist(request):
    print('in userlist',request.data)
    if request.data:
        if request.data['auth']:
            print("yes")
            allusers = User.objects.all()
            serializer = UserSerializers(allusers,many=True)
            print(allusers)
            print(serializer.data)
            return Response(serializer.data)
    else:
        print("no")
        return Response("Not authenticated")
    


@api_view(['PUT'])
def edituser(request,id):
    print('in edit',id)
    print('ddata',request.data)
    data=request.data
    
    try:
        user=User.objects.get(id=id)
        data['password'] = user.password
        print('ko',data)
    except:
        return Response('User not found in the data')
    editserializer=UserSerializers(user,data)
    if editserializer.is_valid():
        editserializer.save()
        check = User.objects.get(id=id)
        print('io',check)
       
        return Response (200)
    return Response(editserializer.errors)


@api_view(['POST'])
def deleteuser(request,id):
    print('in edit',id)
    print('ddata',request.data)
    data=request.data
    
    try:
        user=User.objects.get(id=id)
        user.delete()
        print('ko',data)
        return Response (200)
    except:
        return Response('User not found in the data')




    



