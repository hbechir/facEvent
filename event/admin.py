from django.contrib import admin
from .models import Event, Question, Answer

# Register your models here.

admin.site.register(Event)
admin.site.register(Question)
admin.site.register(Answer)
