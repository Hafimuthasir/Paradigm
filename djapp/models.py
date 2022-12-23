from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50)
    email           = models.EmailField(max_length=100, unique=True)
    profile         = models.FileField(upload_to='C:/Users/AKAM/Desktop/React/week2/djangoproject/reactapp/src/uploads/profile',null=True)
    bio             = models.CharField(max_length=500)
    # required
    date_joined     = models.DateTimeField(auto_now_add=True,null=True)
    last_login      = models.DateTimeField(auto_now_add=True,null=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    is_superadmin    = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def get_first_name(self):
        return self.first_name

    def get_profile(self):
        return self.profile


class Posts(models.Model):
    userid = models.ForeignKey(User,related_name="owner",on_delete=models.CASCADE)
    file = models.FileField(upload_to='C:/Users/AKAM/Desktop/React/week2/djangoproject/reactapp/src/uploads/posts')
    caption = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)



class Story(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    file = models.FileField(upload_to='C:/Users/AKAM/Desktop/React/week2/djangoproject/reactapp/src/uploads/story')
    created_at = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=False)


class Comment(models.Model):
    userid = models.ForeignKey(User,related_name='used',on_delete=models.CASCADE)
    postid = models.ForeignKey(Posts,related_name='comment',on_delete=models.CASCADE)
    comments = models.CharField(max_length=1000)
    
class Likes(models.Model):
    post = models.ForeignKey(Posts,related_name='like',on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    

class Follow(models.Model):
    following = models.ForeignKey(User,related_name="following",on_delete=models.CASCADE)
    follower = models.ForeignKey(User,related_name="follower",on_delete=models.CASCADE)

    # def follow_count(self):
    #     return self.follower.count()