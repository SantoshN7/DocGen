from django.contrib import admin

# Register your models here.
from .models import Student, Course, Document, Student_Course, Student_Document_log

admin.site.register(Student)

admin.site.register(Course)

admin.site.register(Document)

admin.site.register(Student_Course)

admin.site.register(Student_Document_log)