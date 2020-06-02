from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import json
# Create your models here.

dropdown = (("None","None"),("APA","APA"),("MLA","MLA"))
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_studentuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.student = True
        user.save(using=self._db)
        return user
        
    def create_teacheruser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.teacher = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.teacher = True
        user.admin = True
        user.student = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50)
    logged_with_ion = models.BooleanField(default=False)
    
    teachers = models.TextField(default=json.dumps({
        "period_1_teacher" : "",
        "period_2_teacher" : "",
        "period_3_teacher" : "",
        "period_4_teacher" : "",
        "period_5_teacher" : "",
        "period_6_teacher" : "",
        "period_7_teacher" : "",
    }))
    
    def set_teachers(self, teacher):
        print(self.teachers)
        self.teachers = json.dumps(teacher)
    def get_teachers(self):
        print(self.teachers)
        return json.loads(self.teachers)
    
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
    
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (GRADUATE, 'Graduate'),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )
    student = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False)
    admin = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def username(self):
        return self.first_name + " " + self.last_name

    def get_identification(self):
        return self.email

    def get_email(self):
        return self.email

    def get_full_name(self):
        return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)

    def get_short_name(self):
        return self.first_name
        
    def get_grade(self):
        return year_in_school

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_student(self):
        return self.student

    @property
    def is_staff(self):
        return self.teacher

    @property
    def is_admin(self):
        return self.admin
        
    objects = UserManager()
    
    

class Essay(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.CharField(max_length=150, default='Random Assignment')
    teacher = models.CharField(max_length=150, default='None')
    title = models.CharField(max_length=500)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    citation_type = models.CharField(max_length=150, choices=dropdown, default="None")
    marked_body = models.TextField(default=body) 
    graded=False
