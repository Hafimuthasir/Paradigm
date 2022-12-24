from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import *
from django.core.files import File
from django.http import HttpResponse
from rest_framework.decorators import api_view
# Create your views here.


@api_view(['GET','POST'])       
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]  
    
    return Response(routes)
   

@api_view(['POST'])
def register(request):
        print('hai',request)
        print("hoi",request.data)
        email = request.data.get('email')
        print ('j',email)
        checkem=User.objects.filter(email=email)
        if checkem:
            return Response('Email already exist')
        else:
            serializer = UserSerializers(data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(200)

# @api_view(['POST'])
# def login(request):
#     print('am login',request.data)
#     email = request.data['email']
#     password = request.data['password']
#     check = User.objects.filter(email=email,password=password).first()
#     if check:
#         user = 'True'
#         print('true')
#     else:
#         user = 'False'
#         print('false')
#     print("hj",check.id)
#     payload = {
#             'id':check.id,
#             'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
#             'iat':datetime.datetime.utcnow()
#         }
#     token = jwt.encode(payload,'secret',algorithm='HS256')

#     response = Response()
        
#     response.set_cookie(key='jwt',value=token,httponly=True)
    
#     response.data = {
#             'jwt':token,
            
#         }
#     print('lllloool')
#     tk = request.COOKIES.get('jwt')
#     print('mm',tk)
#     print('lll',response)
#     dec = jwt.decode(token,'secret',algorithms='HS256')
#     print ('ds',dec)
#     return response



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.first_name
        token['is_admin'] = user.is_admin
        if user.profile:
            token['profile'] = user.profile.url
        else:
            token['profile'] = "null"

        # ...
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
        
    

@api_view(['GET'])
def userhome(request):
    print('in userhome')
    return Response(200)

@api_view(['POST'])
def uploadPost(request):
    print('in up post')
    print(request.data)
    serializer = PostSerializer(data=request.data,partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
  
    return Response(200)


@api_view(['POST'])
def uploadStory(request):
    print('in up story')
    print(request.data)
    serializer = StorySerializer(data=request.data,partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save() 
    return Response(200)

@api_view(['GET'])
def feedPosts(request):
    print('lol in feed')
    allPost = Posts.objects.all().order_by('-id')
    serializer = PostSerializer(allPost,many=True)
    print('hai')

    # test = serializer.data
    # mydict = {k: test(v).encode("utf-8") for k,v in mydict.iteritems()}
    
    # test2 = test.decode('utf-16')
    # print(test2)
    return Response(serializer.data)

@api_view(['GET'])
def getStory(request):
    print('lol in stry',request.data)
    allUsers = User.objects.all()
    serializer=UserSerializers(allUsers,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def subComment(request):
    print('lol in com',request.data)
    serializer=CommentSerializer(data=request.data,partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response('hai')


@api_view(['POST'])
def LikePost(request):
    print('in like maahn',request.data['user'])
    user = request.data['user']
    post = request.data['post']
    
    exist = Likes.objects.filter(user=user,post=post)
    if exist:        
        exist.delete()
        likecount = Posts.objects.get(id=post)
        print('jii',likecount.likes)
        if int(likecount.likes) > 0:
            likecount.likes=likecount.likes-1
            likecount.save()
        return Response('unliked')
        
    else :
        print('in like')
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        likecount = Posts.objects.get(id=post)
        likecount.likes=int(likecount.likes)+1
        likecount.save()
        return Response('Liked')
       

    # allPost = User.objects.all()
    # serializer = UserSerializers(allPost,many=True)
    # print("joi",serializer.data)

    
@api_view(['GET'])
def getUserPosts(request,id):
    print('lol in ere',id)
    # user = User.objects.get(id=id)
    posts = Posts.objects.filter(userid=id).order_by("-id")
    print('hello',posts)
    serializers = PostSerializer(posts,many=True)
    print('looool',serializers.data)
    return Response(serializers.data)
    

@api_view(['GET'])
def getProfileDatas(request,userid):
    print('lol in profiledatas',id)
    # user = User.objects.get(id=id)
    user = User.objects.get(id=userid)
    print('hello',user)
    serializers = UserSerializers(user,many=True)
    return Response(200)



@api_view(['POST'])
def follow(request):
    print('lol in follow',request.data)
    check = Follow.objects.filter(follower=request.data['follower'],following = request.data['following'])
    print('ppppp',check)
    if check:
        print('intru')
        check.delete()
        return Response('unfollowed')
    else:
        print('infals')
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('followed')
        else:
            print(serializer.errors)
            return Response(serializer.errors)
            

@api_view(['POST'])
def followCheck(request):
    check = Follow.objects.filter(follower=request.data['follower'],following = request.data['following'])
    print('ppppp',check)
    if check:
        return Response('Following')
    else:
        return Response('Follow')

@api_view(['GET'])
def ProfileCounts(request,id):
    # print('6666666',id)
    # following = Follow.objects.filter(follower=id)
    # followers = Follow.objects.filter(following=id)
    # print('followingggggggggggggggg',following,end='')
    # for i in following:
    #     print(i.following.id)
    # print('lllll')
    # for j in followers:
    #     print(j.follower.id)
    # print('followerrrrrrrrrrrrrrrrr',followers)

    uss = User.objects.get(id=id)
    serializer = UserSerializers(uss)
    print('999999999999999999',serializer.data)
    return Response(serializer.data)
    # followers = 
    
    # return Response(200)
    # if check:
    #     return Response('Following')
    # else:
    #     return Response('Follow')



# @api_view(['GET'])
# def DownloadFile(self):
#     path_to_file = 'reactapp/src/uploads/zpostfile' + '/FACE_MASK_fG5rUZ1.rar'
#     f = open(path_to_file, 'rb')
#     pdfFile = File(f)
#     response = HttpResponse(pdfFile.read())
#     response['Content-Disposition'] = 'attachment;'
#     return response


@api_view(['POST'])
def dummyPurchase(request):
    data=request.data
    serializer = PrimeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if serializer.is_valid:
        serializer.save()
        return Response('success')
    return Response(serializer.errors)
    
    

@api_view(['GET'])
def DownloadFile(self,filename):
    print('0000000000',filename)
    # with open('reactapp/src/uploads/zpostfile/FACE_MASK_fG5rUZ1.rar') as f:
    zip_file = open('reactapp/src/uploads/zpostfile/'+filename, 'rb')
    response = HttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'foo.zip'
    return response