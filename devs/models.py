# from django.db import models

# # Create your models here.

# from django.contrib.auth.models import User


# class City(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name


# class Level(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name


# class Availability(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name


# class WorkPreference(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name

# class Skill(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name


# class Industry(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name

# class Vibe(models.Model):
#     name = models.CharField(max_length=150, unique=True)

#     def __str__(self):
#         return self.name
    


# class Developer(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)

#     about = models.TextField(blank=True)
#     portfolio = models.URLField(blank=True)
#     linkedin = models.URLField(blank=True)
#     github = models.URLField(blank=True)

#     city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
#     level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
#     availability = models.ForeignKey(Availability, on_delete=models.SET_NULL, null=True)
#     work_preference = models.ForeignKey(WorkPreference, on_delete=models.SET_NULL, null=True)

#     projects = models.TextField(blank=True)

#     # 🔥 MANY-TO-MANY relationships (your toggle groups)
#     skills = models.ManyToManyField(Skill, blank=True)
#     industries = models.ManyToManyField(Industry, blank=True)
#     vibes = models.ManyToManyField(Vibe, blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


from django.db import models
from django.contrib.auth.models import User

class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name="skills"
    )


    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Vibe(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Developer(models.Model):
    LEVEL_CHOICES = [
        ("junior", "Junior"),
        ("mid", "Mid-level"),
        ("senior", "Senior"),
    ]

    AVAILABILITY_CHOICES = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("freelance", "Freelance"),
    ]

    WORK_PREF_CHOICES = [
        ("remote", "Remote"),
        ("onsite", "On-site"),
        ("hybrid", "Hybrid"),
    ]

    CITY_CHOICES = [
        ("perth", "Perth"),
        ("brisbane", "Brisbane"),
        ("melbourne", "Melbourne"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    city = models.CharField(max_length=100, choices=CITY_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    about = models.TextField(blank=True)
    projects = models.TextField(blank=True)

    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES)
    work_preference = models.CharField(max_length=20, choices=WORK_PREF_CHOICES)

    portfolio = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    skills = models.ManyToManyField(Skill, blank=True)
    industries = models.ManyToManyField(Industry, blank=True)
    vibes = models.ManyToManyField(Vibe, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()