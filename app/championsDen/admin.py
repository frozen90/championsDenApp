from django.contrib import admin
from .models import Profile,Course,Course_Section,Tutor,Message,Feedback
# Register your models here.

admin.site.register(Profile)
admin.site.register(Tutor)
admin.site.register(Course)
admin.site.register(Course_Section)
admin.site.register(Message)
admin.site.register(Feedback)
