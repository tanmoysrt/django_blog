import json
from datetime import datetime,timedelta

from django.core.files.storage import FileSystemStorage
from django.http import  HttpResponse
from django.shortcuts import render

from adminuser.decorators import admin_required, superadmin_required
from normaluser import  models
import random



# Create your views here.
from normaluser.utils import send_mail


@admin_required
def dashoard(request):
    data = {}

    currentdatetime = datetime.now()
    new_posts_today = models.Blog.objects.filter(user_id=request.user.id).filter(created_on__day=currentdatetime.day,created_on__month=currentdatetime.month,created_on__year=currentdatetime.year)
    all_posts = models.Blog.objects.filter(user_id=request.user.id)
    total_views_today = 0
    total_views = 0
    for i in new_posts_today:
        total_views_today+= i.views
    for i in all_posts:
        total_views += i.views

    data["new_posts_count_today"] = len(new_posts_today)
    data["all_posts_count"] = len(all_posts)
    data["total_views_today"] = total_views_today
    data["total_views"] = total_views

    list_of_dates = []
    list_of_blogs = []
    for i in range(0,7)[::-1]:
        list_of_dates.append(str((currentdatetime-timedelta(days=i)).date()))
        list_of_blogs.append(len(models.Blog.objects.filter(user_id=request.user.id).filter(created_on__day=(currentdatetime-timedelta(days=i)).day,created_on__month=(currentdatetime-timedelta(days=i)).month,created_on__year=(currentdatetime-timedelta(days=i)).year)))

    data["list_of_blogs"]=json.dumps(list_of_blogs)
    data["list_of_dates"]=json.dumps(list_of_dates)
    return render(request,"adminuser/dashboard.html",data)

@admin_required
def deletePost(request,postid):
    message = ""
    try:
        record = models.Blog.objects.get(id=postid)
        if request.user.category == "superadmin" or request.user.id == record.user_id:
            record.delete()
            message = '''<div class="alert alert-success" role="alert">Post Deleted Successfully</div>'''
        else:
            message = '''<div class="alert alert-warning" role="alert">You have no permission to delete this post.</div>'''
    except:
        message = '''<div class="alert alert-danger" role="alert">Post Delete Failed !! Retry</div>'''

    return  message

# All posts [OWN + Other memebers]
@superadmin_required
def allpost(request):
    data = {
        "posts" : models.Blog.objects.all().order_by("-id")
    }
    if "delete" in request.GET:
        id = request.GET.get("delete",0)
        message = deletePost(request,id)
        data["message"]=message

    return render(request,"adminuser/allpost.html",data)

# All owned posts
@admin_required
def ownedposts(request):
    data = {
        "posts" : models.Blog.objects.filter(user_id=request.user.id).order_by("-id")
    }
    if "delete" in request.GET:
        id = request.GET.get("delete",0)
        message = deletePost(request,id)
        data["message"]=message

    return render(request,"adminuser/ownedpost.html",data)

# Normal Function
def generate_random_filename(filename):
    extension = str(filename).split(".")[-1]
    random_name = str(random.randint(1111111111111111,9999999999999999))
    final_random_name = random_name+"."+extension
    return final_random_name

# Create New Post
@admin_required
def newpost(request):
    data={
        "categories" : models.BLOG_CATEGORY
    }
    if request.method == "POST" and request.FILES["thumbnail"]:
        thumbnail = request.FILES['thumbnail']
        fs = FileSystemStorage(location='media/')
        filename = fs.save(generate_random_filename(thumbnail.name), thumbnail)
        photoname = fs.generate_filename(filename)

        title = request.POST.get("title","")
        tags = request.POST.get("tags","")
        category = request.POST.get("category","")
        description = request.POST.get("description","")
        content = request.POST.get("content","")

        try:
            record = models.Blog.objects.create(
                user=request.user,
                title=title,
                description=description,
                content=content,
                category=category,
                tags=tags,
                thumbnail=photoname
            )
            record.save()
            data["message"]=f'''<div class="alert alert-success" role="alert">Post Created Successfull <a target="_blank" href="/blog/{record.id}/">Click Here To See</a></div>'''
        except:
            data["message"]='''<div class="alert alert-danger" role="alert">Failed ! Retry</div>'''
    return render(request,"adminuser/createpost.html",data)

# Edit Post
@admin_required
def editpost(request,id):
    try:
        record = models.Blog.objects.get(id=id)
    except:
        return HttpResponse("Blog Not Found !!!")
    data={
        "blog":record,
        "categories":models.BLOG_CATEGORY
    }
    if request.user.category != "superadmin" and  record.user_id != request.user.id:
        return  HttpResponse("You have no access to edit the post")

    if request.method == "POST":
        title = request.POST.get("title","")
        tags = request.POST.get("tags","")
        category = request.POST.get("category","")
        description = request.POST.get("description","")
        content = request.POST.get("content","")
        try:
            record.title = title
            record.tags = tags
            record.category = category
            record.description = description
            record.content = content
            record.save()

            if request.FILES:
                if "thumbnail" in request.FILES:
                    thumbnail = request.FILES['thumbnail']
                    fs = FileSystemStorage(location='media/')
                    filename = fs.save(generate_random_filename(thumbnail.name), thumbnail)
                    photoname = fs.generate_filename(filename)
                    record.thumbnail = photoname
                    record.save()
            data["message"]=f'''<div class="alert alert-success" role="alert">Post Updated Successfull <a target="_blank" href="/blog/{record.id}/">Click Here To See</a></div>'''
        except:
            data["message"]='''<div class="alert alert-danger" role="alert">Failed ! Retry</div>'''

    return render(request,"adminuser/editpost.html",data)

# List of all users
@superadmin_required
def users(request):
    data = {
        "users":models.CustomUser.objects.all()
    }
    return render(request,"adminuser/userslist.html",data)

#  Add User Admin
@superadmin_required
def adduser(request):
    data = {
        "usercategories":models.USER_CATEGORY
    }
    if request.method == "POST":
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        category = request.POST.get("category","normal")
        password = random.randint(123456789,999999999)

        if len(models.CustomUser.objects.filter(email=email)) == 0 :
            try:
                models.CustomUser.objects.create_user(
                    name=name,
                    email=email,
                    category=category,
                    password=password
                )
                send_mail(email,f"Your default password is {password}. Kindly login.")
                data["message"]= '''<div class="alert alert-success" role="alert">Account Created Successfully</div>'''
            except Exception as e:
                print(e)
                data["message"]= '''<div class="alert alert-danger" role="alert">Failed !</div>'''
        else:
            data["message"] = '''<div class="alert alert-warning" role="alert">Email Already Exsists !</div>'''

    return render(request,"adminuser/adduser.html",data)

# Subscriptions
@superadmin_required
def subscriptions(request):
    data={
        "subscriptions":models.Subscriptions.objects.all().order_by("-id")
    }
    return render(request,"adminuser/subscriptions.html",data)

# Contacus submissions list
@superadmin_required
def contactus(request):
    data={
        "contactusrequest":models.ContactUs.objects.all().order_by("-id")
    }
    return render(request,"adminuser/contactus.html",data)