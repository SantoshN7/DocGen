from django.db import models


# Create your models here.

class Student(models.Model):
    gender_choice = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    s_name = models.CharField(max_length=255)
    s_email = models.EmailField(unique=True)
    s_mobile = models.BigIntegerField(unique=True)
    s_eligibility = models.BigIntegerField(unique=True)
    s_birth_date = models.DateTimeField()
    s_gender = models.CharField(choices=gender_choice,max_length=8)

    def __str__(self):
        return self.s_name



class Course(models.Model):
    c_name = models.CharField(max_length=255)
    c_fee = models.FloatField()

    def __str__(self):
        return self.c_name

class Document(models.Model):
    d_name = models.CharField(max_length=255)

    def __str__(self):
        return self.d_name


class Student_Course(models.Model):
    fee_choices = [
        ('Pending', 'Pending'),
        ('Full Paid', 'Full Paid'),
    ]
    status_choices = [
        ('Ongoing','Ongoing'),
        ('Completed','Completed'),
    ]
    s_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    c_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    fee_status = models.CharField(default='Full Paid',choices=fee_choices, max_length=20)
    course_status = models.CharField(default='Ongoing',choices=status_choices, max_length=20)
    roll_no = models.IntegerField(unique=True)
    e_year = models.CharField(blank=True,null=True,max_length=10)
    e_seat_no = models.IntegerField(blank=True,null=True)
    e_result = models.CharField(blank=True,null=True,max_length=10)
    


class Student_Document_log(models.Model):
    s_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    d_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    genrated_time = models.DateTimeField(auto_now_add=True)


