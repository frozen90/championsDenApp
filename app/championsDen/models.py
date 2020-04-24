from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

GRADE_CHOICES =(
    ('Excellent', 'A'),
    ('Overall Good', 'B'),
    ('Poor', 'C'),
    ('Very Poor', 'D'),
)

REGION_CHOICES =(
    ("BR1", "Brazil"),
    ("EUN1", "EU Nordic East"),
    ("EUW1", "EU West"),
    ("JP1", "Japan"),
    ("KR", "Korea"),
    ("LA1", "Latin America 1"),
    ("LA2", "Latin America 2"),
    ("NA1", "North America"),
    ("OC1", "Oceania"),
    ("TR1", "Turkey"),
    ("RU", "Russia"),

)

ROLE_CHOICES = (
    ('MID','MIDLANE'),
    ('TOP','TOPLANE'),
    ('JUNGLE','JUNGLE'),
    ('BOT','BOTLANE'),
    ('SUPPORT','SUPPORT'),
    ('ALL','ALL')
)

SKILL_CHOICES = (
    ('BEGINNER','BEGINNER'),
    ('INTERMEDIATE','INTERMEDIATE'),
    ('EXPERT','EXPERT'),
    ('ALL','ALL'),

)

class Message(models.Model):

    subject = models.CharField(max_length=300, null=True);
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True);
    receiver = models.ForeignKey(User,related_name="message_receiver", on_delete=models.CASCADE, null=True);
    body = models.TextField(max_length=1000,null=True);
    new_message = models.BooleanField(default=True);

    def __str___(self):
        return self.subject


class Feedback(models.Model):

    grade = models.CharField(max_length=7, choices=REGION_CHOICES,null=True);
    feedback_sender = models.ForeignKey(User, on_delete=models.CASCADE,null=True);
    feedback_receiver = models.ForeignKey(User, related_name="feedback_receiver", on_delete=models.CASCADE, null=True);
    feedback_given = models.BooleanField(default=False);

    def __str__(self):
        return self.sender



class Tutor(models.Model):

    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100);
    region = models.CharField(max_length=15, choices=REGION_CHOICES);
    date_of_birth = models.DateField()
    profile_pic = models.ImageField(upload_to='tutor_profile_pic/' , max_length=100)
    stripe_acc_id = models.CharField(max_length=100);
    summoner_name = models.CharField(max_length=100);
    rank = models.CharField(max_length=100);

    def __str__(self):
        return self.user.username




class Profile(models.Model):

    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    summoner_name = models.CharField( max_length=100);
    region = models.CharField(max_length=4, choices=REGION_CHOICES);



    def __str__(self):
        return self.user.username


class Course(models.Model):

    course_name = models.CharField("course name", max_length=100);
    course_author = models.CharField("course author", null=False, max_length=100);
    description = models.TextField(max_length=10000);
    role = models.CharField(max_length=10, choices=ROLE_CHOICES);
    tags = models.CharField(max_length=100);
    experience = models.CharField(max_length=15, choices=SKILL_CHOICES);
    rank = models.CharField(max_length=150);
    price = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(1)]);
    users_with_access = models.ManyToManyField(User, blank=True);
    image_field = models.ImageField(upload_to='courses_logo/' , max_length=100);
    ratings = GenericRelation(Rating, related_query_name='Courses');
    last_updated = models.DateField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    buys = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.course_name


    @classmethod
    def subscribe(cls, current_user, new_course):
        new_course.users_with_access.add(current_user)

    @classmethod
    def unsubscribe(cls,current_user, cancel_course):
        cancel_course.users_with_access.remove(current_user)


class Course_Section(models.Model):

    course_id = models.ForeignKey(Course, on_delete=models.CASCADE);
    section_title = models.CharField("section title", max_length=100);
    video_url = models.URLField(max_length=250);
    section_description = models.TextField("section description", max_length=1000);
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.section_title
