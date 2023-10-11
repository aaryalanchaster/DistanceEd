from django.contrib import admin
from django.db import models
from .models import Category, Course, Student, Instructor

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Instructor)
