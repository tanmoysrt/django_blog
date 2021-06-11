from django.urls import path, include
from . import views

# - /
#     - / [homepage]
#     - blog/<int:id>/
#     - category/  [WORK THROUGH GET REQUEST][SEARCH ALSO INCLUDED HERE]
#     - contact-us/
#     - login/
#     - logout/
#     - register/
#     - contact-us/
#     - reset-pass/
#     - reset-link/<str:resetkey>/
#     - search/

urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("category/", views.category, name="blogcategory"),
    path("login/",views.loginUser,name="login"),
    path("logout/",views.logoutUser,name="logout"),
    path("register/",views.registerUser,name="register"),
    path("contact-us/",views.contactus,name="contatcus"),
    path("reset-pass/",views.forgetPasswordRequest,name="forgetpasswordrequest"),
    path("reset-link/<str:resetkey>/",views.forgetPasswordConfirm,name="forgetpasswordconfirm"),
    # Place always slug field at the last of all routes
    # So that it does not conflict with other route
    path("blog/<int:id>/", views.blog, name="fullblog"),
    path("search/",views.search,name="searchpage"),
    path("charge/",views.payandsubscribe)
]