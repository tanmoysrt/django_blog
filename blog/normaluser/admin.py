from django.contrib import admin
from . import  models

admin.site.register(models.CustomUser)
admin.site.register(models.Blog)
admin.site.register(models.Comments)
admin.site.register(models.Subscriptions)
admin.site.register(models.ContactUs)
