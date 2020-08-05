from django.contrib import admin
from . models import Users, FeedbackUser
# Register your models here.

admin.site.register(Users)
admin.site.register(FeedbackUser)