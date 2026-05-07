from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random

from devs.models import (
    Developer,
    Skill,
    SkillCategory,
    Industry,
    Vibe,
)
from projects.models import Project

fake = Faker()


SKILL_CATEGORIES = [
    {
        "label": "Frontend",
        "skills": ["HTML/CSS", "JavaScript", "TypeScript", "React"],
    },
    {
        "label": "Backend",
        "skills": ["Node.js", "Python", "Django", "Ruby on Rails", "PHP", "Laravel"],
    },
    {
        "label": "Database & Cloud",
        "skills": ["PostgreSQL", "MySQL", "REST APIs"],
    },
    {
        "label": "Design",
        "skills": ["UI/UX Design"],
    },
    {
        "label": "Platform & CMS",
        "skills": ["Shopify", "WordPress"],
    },
]



class Command(BaseCommand):
    help = "Seed database with fake developers and projects"

    
    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding data...")

        Project.objects.all().delete()
        Developer.objects.all().delete()
        User.objects.all().delete()

        Skill.objects.all().delete()
        SkillCategory.objects.all().delete()


        # -------------------------
        # Create skills and categories
        # -------------------------

        for category_data in SKILL_CATEGORIES:
            category_name = category_data["label"]

            # create or get category
            category, created = SkillCategory.objects.get_or_create(
                name=category_name
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category_name}"))

            for skill_name in category_data["skills"]:
                skill, created = Skill.objects.get_or_create(
                    name=skill_name,
                    category=category
                )

                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"  ↳ Created skill: {skill_name}")
                    )

        # -------------------------
        # Create lookup data
        # -------------------------
        # skills = ["HTML/CSS", "JavaScript", "TypeScript", "React","Node.js", "Python", "Django", "Ruby on Rails", "PHP", "Laravel","PostgreSQL", "MySQL", "REST APIs","UI/UX Design","Shopify", "WordPress"]
        industries = ["Health & Wellness", "Fintech", "Ecommerce", "Education", "Nonprofit"]
        vibes = [ "I work best async",
            "I love early-stage chaos",
            "I'm a finisher not just a starter",
            "I care about design details",
            "I move fast and iterate",
            "I love a good brief",
            "I prefer long-term projects",
            "I'm great at explaining tech to non-techies",
            "I'm a solo operator",
            "I love collaborating",
            "I build for impact",
            "I'm obsessed with clean code",]

        # skill_objs = [Skill.objects.get_or_create(name=s)[0] for s in skills]

        skill_objs = list(Skill.objects.all())

        industry_objs = [Industry.objects.get_or_create(name=i)[0] for i in industries]
        vibe_objs = [Vibe.objects.get_or_create(name=v)[0] for v in vibes]

        developers = []

        # -------------------------
        # Create developers
        # -------------------------
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )

            dev = Developer.objects.create(
                user=user,
                #city=fake.city(),
                city=random.choice([c[0] for c in Developer.CITY_CHOICES]),
                level=random.choice(["junior", "mid", "senior"]),
                about=fake.text(),
                availability=random.choice(["full_time", "part_time", "freelance"]),
                work_preference=random.choice(["remote", "onsite", "hybrid"]),
                portfolio=fake.url(),
                linkedin=f"https://linkedin.com/in/{fake.user_name()}",
                github=f"https://github.com/{fake.user_name()}",
            )

            dev.skills.set(random.sample(skill_objs, k=random.randint(1, 3)))
            dev.industries.set(random.sample(industry_objs, k=random.randint(1, 2)))
            dev.vibes.set(random.sample(vibe_objs, k=random.randint(1, 2)))

            developers.append(dev)

        # -------------------------
        # Create projects
        # -------------------------
        for _ in range(10):
          
            owner = random.choice(developers).user

            project = Project.objects.create(
                title=fake.catch_phrase(),
                description=fake.text(),
                owner=owner,
                city=random.choice([c[0] for c in Project.CITY_CHOICES]),
                type=random.choice([c[0] for c in Project.TYPE_CHOICES]),
                budget=random.choice([c[0] for c in Project.BUDGET_CHOICES]),
                timeline=random.choice([c[0] for c in Project.TIMELINE_CHOICES]),
                stage=random.choice([c[0] for c in Project.STAGE_CHOICES]),
            )

            project.skills_needed.set(random.sample(skill_objs, k=random.randint(1, 3)))
            project.industries.set(random.sample(industry_objs, k=random.randint(1, 2)))
            

            # assign devs to project (if you have M2M)
            if hasattr(project, "developers"):
                project.developers.set(
                    random.sample(developers, k=random.randint(1, 3))
                )

        self.stdout.write(self.style.SUCCESS("✅ Seeding complete!"))