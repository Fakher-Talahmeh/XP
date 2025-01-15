from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

user = get_user_model()
class Profile(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    join_date = models.DateTimeField(default=timezone.now)
    function = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Family(models.Model):
    family_code = models.CharField(max_length=50, unique=True)
    geographical_origin = models.CharField(max_length=100)
    num_individuals = models.PositiveIntegerField()

    def __str__(self):
        return self.family_code

class Individual(models.Model):
    STATUS_CHOICES = [
        ('patient', 'Patient'),
        ('carrier', 'Carrier'),
        ('unaffected', 'Unaffected'),
    ]
    
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    date_of_birth = models.DateField()
    kinship = models.CharField(max_length=50)
    geographical_origin = models.CharField(max_length=100)
    consanguinity = models.BooleanField(default=False)
    family_history = models.BooleanField(default=False)
    age_at_study = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.family.family_code} - Individual {self.id}"

class Forum(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=200)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address} ({self.latitude}, {self.longitude})"

class Documentation(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/', null=True, blank=True)

    def __str__(self):
        return self.title