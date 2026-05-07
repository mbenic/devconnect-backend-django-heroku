# project models
from projects.models import Project

# dev models
from devs.models import (
    Developer,
    Industry,
    Vibe,
    SkillCategory
     
)
from devs.serializers import SkillSerializer

from rest_framework.views import APIView
from rest_framework.response import Response




class ChoicesView(APIView):
    def get(self, request):
        def format_choices(choices):
            # return [
            #     {"value": key, "label": label}
            #     for key, label in choices
            # ]
            return [
                {"id": key, "name": label}
                for key, label in choices
            ]
        
        def to_dropdown(queryset):
            # return [{"value": obj.id, "label": obj.name} for obj in queryset]
            return [{"id": obj.id, "name": obj.name} for obj in queryset]


        data = {
            "city": format_choices(Project.CITY_CHOICES),
            "type": format_choices(Project.TYPE_CHOICES),
            "budget": format_choices(Project.BUDGET_CHOICES),
            "timeline": format_choices(Project.TIMELINE_CHOICES),
            "stage": format_choices(Project.STAGE_CHOICES),


        # "skills": to_dropdown(Skill.objects.all()),

# # 🔥 GROUPED SKILLS (matches frontend exactly)
            "skills": [
                {
                    "label": category.name,
                    # "skills": [skill.name for skill in category.skills.all()]
                    "skills": SkillSerializer(category.skills.all(), many=True).data
                }
                for category in SkillCategory.objects.prefetch_related("skills").all()
            ],

            "industries": to_dropdown(Industry.objects.all()),
            "vibes": to_dropdown(Vibe.objects.all()),
            "levels": format_choices(Developer.LEVEL_CHOICES),
            "availabilities": format_choices(Developer.AVAILABILITY_CHOICES),
            "work_preferences": format_choices(Developer.WORK_PREF_CHOICES),
            

        }

        return Response(data)
    

