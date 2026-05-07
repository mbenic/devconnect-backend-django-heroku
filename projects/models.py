from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):

    CITY_CHOICES = [
        ("perth", "Perth"),
        ("brisbane", "Brisbane"),
        ("melbourne", "Melbourne"),
    ]

    TYPE_CHOICES = [
        ("paid", "Paid"),
        ("volunteer", "Volunteer"),
    ]

    BUDGET_CHOICES = [
        ("under_500", "Under $500"),
        ("over_500", "Over $500"),
     
    ]

    TIMELINE_CHOICES = [
        ("1_2_weeks", "1-2 weeks"),
        ("3_4_weeks", "3-4 weeks"),
        ("1_3_months", "1-3 months"),
    ]

    STAGE_CHOICES = [
        ("idea", "Just an idea"),
        ("mvp", "MVP"),
        ("launched", "Launched"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")

    title = models.CharField(max_length=255)
    description = models.TextField()

    city = models.CharField(max_length=100, choices=CITY_CHOICES)

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES)
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)

    skills_needed = models.ManyToManyField("devs.Skill", blank=True)
    industries = models.ManyToManyField("devs.Industry", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
