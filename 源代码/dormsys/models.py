from django.db import models

# user system
class User(models.Model):
    member_id = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=20)


# Create your models here.
class Student(models.Model):
    student_number = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    in_year = models.CharField(max_length=20)
    tutor_number = models.CharField(max_length=20)

class Department_Student(models.Model):
    student_number = models.CharField(max_length=20)
    department_number = models.CharField(max_length=20)

class DormDistribution(models.Model):
    student_number = models.CharField(max_length=20)
    room_number = models.CharField(max_length=20)
    apartment_number = models.CharField(max_length=20)


class Room(models.Model):
    room_number = models.CharField(max_length=20)
    apartment_number = models.CharField(max_length=20)
    rest_num = models.IntegerField(default=4)


class Apartment(models.Model):
    apartment_number = models.CharField(max_length=20)
    apartment_type = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    apartment_name = models.CharField(max_length=20)
    capacity = models.IntegerField()
    bathroom = models.CharField(max_length=20)
    washroom = models.CharField(max_length=20)

class DormAdmin(models.Model):
    name = models.CharField(max_length=20)
    supervisor_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    apartment_number = models.CharField(max_length=20)

class Tutor(models.Model):
    name = models.CharField(max_length=20)
    tutor_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    department_number = models.CharField(max_length=20)

class Department(models.Model):
    department_number = models.CharField(max_length=20)
    department_name = models.CharField(max_length=20)
    school_name = models.CharField(max_length=20)

class EmergencyContact(models.Model):
    student_number = models.CharField(max_length=20)
    relation = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    emergency_name = models.CharField(max_length=20)


# approval
class EnterDorm(models.Model):
    student_number = models.CharField(max_length=20)
    room_number = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    apartment_name = models.CharField(max_length=20)
    tutor_number = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    apply_time = models.DateTimeField(auto_now_add=True)
    deal_time = models.DateTimeField(null=True)

class QuitDorm(models.Model):
    student_number = models.CharField(max_length=20)
    room_number = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    tutor_number = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    apply_time = models.DateTimeField(auto_now_add=True)
    deal_time = models.DateTimeField(null=True)

class ChangeDorm(models.Model):
    student_number = models.CharField(max_length=20)
    room_number = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    apartment_name = models.CharField(max_length=20)
    tutor_number = models.CharField(max_length=20)

    state = models.CharField(max_length=20)
    apply_time = models.DateTimeField(auto_now_add=True)
    deal_time = models.DateTimeField(null=True)

class Approval(models.Model):
    student_number = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    room_number = models.CharField(max_length=20,null=True)
    region = models.CharField(max_length=20,null=True)
    apartment_name = models.CharField(max_length=20,null=True)
    tutor_number = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    apply_time = models.DateTimeField(auto_now_add=True)
    deal_time = models.DateTimeField(null=True)
    type = models.CharField(max_length=20)

# announcement

class Announcement(models.Model):
    content = models.CharField(max_length=100)
    supervisor_number = models.CharField(max_length=20)
    issue_time = models.DateTimeField(auto_now_add = True)
