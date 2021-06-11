from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import models
import json
import secrets
import string
import razorpay

# Homepage of blog
def homepage(request):
    data={
        "trending":models.Blog.objects.all().order_by("-views")[0:21],
        "allposts":models.Blog.objects.all().order_by("-created_on")
    }
    return render(request,"normaluser/homepage.html",data)

# Category wise blogs
def category(request):
    data = {
        "category":models.BLOG_CATEGORY[1:]
    }
    data["blogs"]=models.Blog.objects.all()
    if "category" in request.GET:
        category = request.GET.get("category","none")
        category_name = None
        for i in models.BLOG_CATEGORY:
            if i[0] == category:
                category_name = i[1]
                break
        if category_name is not None:
            data["selected_category_name"]=category_name
            data["blogs"]=data["blogs"].filter(category=category)
    return render(request,"normaluser/category.html",data)

# Full blog content
def blog(request,id):
    data = {}
    blog = models.Blog.objects.get(id=id)
    blog.views += 1
    blog.save()

    if "like" in request.GET:
        if not request.user.is_authenticated:
            return redirect("/login/")
        like = request.GET.get("like","-1")
        if like != "-1":
            if like == "1":
                likes = list(json.loads(blog.likes))
                if not request.user.id in likes:
                    likes.append(request.user.id)
                    blog.likes = json.dumps(likes)

                dislikes = list(json.loads(blog.dislikes))
                if request.user.id in dislikes:
                    dislikes.remove(request.user.id)
                    blog.dislikes = json.dumps(dislikes)

            elif like == "0":
                likes = list(json.loads(blog.likes))
                if request.user.id in likes:
                    likes.remove(request.user.id)
                    blog.likes = json.dumps(likes)

                dislikes = list(json.loads(blog.dislikes))
                if not request.user.id in dislikes:
                    dislikes.append(request.user.id)
                    blog.dislikes = json.dumps(dislikes)
            blog.save()

    if request.method == "POST":
        comment = request.POST.get("comment","")
        if comment is not None:
            blog.comments.create(
                comment=comment,
                name = request.user.name
            )

    data["blog"] = blog
    data["likescount"] = len(json.loads(blog.likes))
    data["dislikescount"] = len(json.loads(blog.dislikes))
    data["comments"]= models.Comments.objects.filter(blog_id=blog.id)

    return render(request,"normaluser/fullblog.html",data)

# Conact Us Page
def contactus(request):
    data = {}
    if request.method == "POST":
        name = request.POST.get("name","")
        email = request.POST.get("email", "")
        phoneno = request.POST.get("phoneno", "")
        message = request.POST.get("message", "")

        models.ContactUs.objects.create(
            name=name,
            email=email,
            phoneno=phoneno,
            message=message
        )
        data["message"]= '''<div class="alert alert-success" role="alert">Query Submitted Successfully ! We will contact you soon</div>'''
    return render(request,"normaluser/contactus.html",data)

# Login User Page
def loginUser(request):
    if request.user.is_authenticated:
        return redirect("/")

    data = {}
    if request.method == "POST":
        email = request.POST.get("email","")
        password = request.POST.get("password","")
        user = authenticate(email= email,password= password)
        if user is not None:
            login(request,user)
            return redirect("/")
        data["message"] = '''<div class="alert alert-danger" role="alert">
                                  Username or Password not matched
                                </div>'''
    return render(request,"normaluser/login.html",data)

# Search Blog Page
def search(request):
    data={}
    if "q" in request.GET:
        query = request.GET.get("q","")
        data["query"]=query
        data["blogs"] = models.Blog.objects.filter(Q(title__icontains=query) | Q(tags__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query))
    else:
        data["blogs"] = models.Blog.objects.all()

    return render(request,"normaluser/search.html",data)

# Logout And Redirect
def logoutUser(request):
    logout(request)
    return redirect("/")

# Register User page
def registerUser(request):
    if request.user.is_authenticated:
        return redirect("/")
    data = {}
    if request.method == "POST":
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        password = request.POST.get("passsword","")
        confirmpassword = request.POST.get("confirmpassword","")

        if password != confirmpassword:
            data["message"] = '''<div class="alert alert-danger" role="alert">Password and Confirm Password Not Matches</div>'''
        else:
            try:
                models.CustomUser.objects.get(email=email)
                data["message"] = '''<div class="alert alert-danger" role="alert">User Already Exsists</div>'''
            except:
                user = models.CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    name = name
                )
                user.save()
                login(request,user)
                return redirect("/")


    return render(request,"normaluser/register.html",data)

# Forget Password Page
def forgetPasswordRequest(request):
    if request.user.is_authenticated:
        return redirect("/")
    data = {}
    if request.method == "POST":
        email = request.POST.get("email","")
        try:
            user = models.CustomUser.objects.get(email=email)
            resetRecord = models.ForgotPasswordDB.objects.create(
                email=user.email,
                key=''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(80)).lower()
            )
            resetRecord.save()
            print(f"http://127.0.0.1:8000/reset-link/{resetRecord.key}")
        except:
            print("No user found")
        data["message"]='''<div class="alert alert-success" role="alert">If you have account in this email id. You will recieve a reset link in mail</div>'''
    return render(request,"normaluser/forgetrequest.html",data)

# Forget Password Check and password change request
def forgetPasswordConfirm(request,resetkey):
    logout(request)
    data= {}
    if resetkey is not None:
        record = models.ForgotPasswordDB.objects.get(key=resetkey)
        if record.is_active:
            data["email"]=record.email

            if request.method == "POST":
                password = request.POST.get("password","")
                confirmpassword = request.POST.get("confirmpassword","")
                if password != confirmpassword:
                    data["message"]='''<div class="alert alert-danger" role="alert">Password & Confirm Password does not match !</div>'''
                else:
                    try:
                        user = models.CustomUser.objects.get(email=record.email)
                        user.set_password(password)
                        user.save()
                        record.is_active = False
                        record.save()
                        data["message"]='''<div class="alert alert-success" role="alert">Password Changed Successfully</div>'''
                    except:
                        data["message"] = '''<div class="alert alert-danger" role="alert">User Not Found/div>'''
        else:
            return redirect("/")

    return render(request,"normaluser/forgetconfirm.html",data)

def payandsubscribe(request):
    razorpay_client = razorpay.Client(auth=("rzp_test_U4ii7u4SIQvK0v", "IH49svMg3mXKTPYnONrnJ7IR"))

    if "payment_id" in request.GET:
        razorpay_client.payment.capture(request.GET.get("payment_id",""),30000)
        log = razorpay_client.payment.fetch(request.GET.get("payment_id",""))
        print(log)
        if log["status"] == "captured":
            try:
                record = models.CustomUser.objects.get(email=log["notes"]["registerd_email"])
                record.category = "admin"
                record.save()
                return redirect("/blog-admin/")
            except:
                return HttpResponse("Unexpected Error")
        return HttpResponse("OK")
    return HttpResponse("Nothing Found")