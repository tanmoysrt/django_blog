from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from normaluser.managers import CustomUserManager

BLOG_CATEGORY = (
    ("none","No Category"),
    ("ml","Machine Learning"),
    ("dl","Deep Learning"),
    ("app","Apps"),
    ("game","Games"),
    ("techupdate","Tech Update")
)

USER_CATEGORY = (
    ("normal","Normal User"), # Have access to like,dislike, Comments
    ("admin","Administrator"), # Have access to like,dislike, Comments, New Post
    ("superadmin","Superadmin")  # All Access
)

class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(_('email address'),unique=True)
    category = models.CharField(max_length=50,choices=USER_CATEGORY,default="normal",null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

class Blog(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="blog")
    title = models.CharField(max_length=300,blank=True,null=True,default="")
    description = models.TextField(null=True)
    content = models.TextField(default="",null=True,blank=True)
    thumbnail = models.TextField(null=True,default="default.jpg")
    category = models.CharField(max_length=80,choices=BLOG_CATEGORY,null=True,default="none")
    tags = models.CharField(max_length=300,blank=True,null=True,default="")
    views = models.IntegerField(default=0,null=True)
    likes = models.TextField(default="[]")
    dislikes = models.TextField(default="[]")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comments(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="comments")
    name = models.TextField(null=True,default="")
    comment = models.TextField(null=True,default="")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class Subscriptions(models.Model):
    email = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class ContactUs(models.Model):
    name = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=100,null=True)
    phoneno = models.CharField(max_length=20,null=True)
    message = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class ForgotPasswordDB(models.Model):
    email  = models.TextField(null=True)
    key = models.TextField(null=True)
    is_active = models.BooleanField(null=True,default=True)
    created_on = models.DateTimeField(auto_now_add=True)