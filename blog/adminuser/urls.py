from django.urls import path, include
from . import views

# - /admin
#     - /    (Show Analytics [DASHBAORD])
#     - allpost/ [ONLY FOR SUPERADMIN]
#     - posts/
#     - newpost/
#     - editpost/<int:id>/
#     - subscriptions/
#     - contact-us/
#     - users/ [CRUD VIEW]
#     - adduser/


urlpatterns = [
    path("",views.dashoard,name="dashboard"),
    path("allpost/",views.allpost,name="allpost"),
    path("posts/",views.ownedposts,name="ownposts"),
    path("newpost/",views.newpost,name="newpost"),
    path("editpost/<int:id>/",views.editpost,name="editpost"),
    path("subscriptions/",views.subscriptions,name="subscriptions"),
    path("contact-us/",views.contactus,name="contact-us"),
    path("users/",views.users,name="users"),
    path("adduser/",views.adduser,name="adduser")
]