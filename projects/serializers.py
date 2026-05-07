from rest_framework import serializers
from .models import Project
from devs.models import Skill, Industry
from django.contrib.auth.models import User


# --- BASIC NESTED SERIALIZERS ---

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ["id", "username"]
        fields = ["id", "first_name", "last_name", "email"]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ["id", "name"]


# --- MAIN SERIALIZER ---

# class ProjectSerializer(serializers.ModelSerializer):

#     # 👤 Owner (read-only)
#     owner = UserBasicSerializer(read_only=True)

#     # ✅ WRITE: accept IDs
#     skills_needed = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Skill.objects.all(),
#         write_only=True
#     )

#     industries = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Industry.objects.all(),
#         write_only=True
#     )

#     # ✅ READ: return full objects
#     skills = SkillSerializer(source="skills_needed", many=True, read_only=True)
#     industries_data = IndustrySerializer(source="industries", many=True, read_only=True)

#     # ✅ Choice display fields
#     city_display = serializers.CharField(source="get_city_display", read_only=True)
#     type_display = serializers.CharField(source="get_type_display", read_only=True)
#     budget_display = serializers.CharField(source="get_budget_display", read_only=True)
#     timeline_display = serializers.CharField(source="get_timeline_display", read_only=True)
#     stage_display = serializers.CharField(source="get_stage_display", read_only=True)

#     class Meta:
#         model = Project
#         fields = [
#             "id",
#             "title",
#             "description",

#             "owner",

#             # raw values (write + read if needed)
#             "city",
#             "type",
#             "budget",
#             "timeline",
#             "stage",

#             # display values
#             "city_display",
#             "type_display",
#             "budget_display",
#             "timeline_display",
#             "stage_display",

#             # relationships
#             "skills_needed",     # write
#             "skills",            # read
#             "industries",        # write
#             "industries_data",   # read

#             "created_at",
#         ]


# --- WRITE SERIALIZER ---
class ProjectWriteSerializer(serializers.ModelSerializer):
    skills_needed = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Skill.objects.all()
    )
    industries = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Industry.objects.all()
    )

    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "city",
            "type",
            "budget",
            "timeline",
            "stage",
            "skills_needed",
            "industries",
        ]



class ProjectReadSerializer(serializers.ModelSerializer):
    owner = UserBasicSerializer()

    # nested relations
    skills = SkillSerializer(source="skills_needed", many=True)
    industries = IndustrySerializer(many=True)

    # choice labels
    city_display = serializers.CharField(source="get_city_display")
    type_display = serializers.CharField(source="get_type_display")
    budget_display = serializers.CharField(source="get_budget_display")
    timeline_display = serializers.CharField(source="get_timeline_display")
    stage_display = serializers.CharField(source="get_stage_display")

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",

            "owner",

            #"city",
            "city_display",

            #"type",
            "type_display",

            #"budget",
            "budget_display",

            #"timeline",
            "timeline_display",

            #"stage",
            "stage_display",

            "skills",
            "industries",

            "created_at",
        ]


    # 🔧 Explicit create (safe + clear)
    def create(self, validated_data):
        skills = validated_data.pop("skills_needed", [])
        industries = validated_data.pop("industries", [])

        project = Project.objects.create(**validated_data)

        project.skills_needed.set(skills)
        project.industries.set(industries)

        return project

    # 🔧 Explicit update
    def update(self, instance, validated_data):
        skills = validated_data.pop("skills_needed", None)
        industries = validated_data.pop("industries", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if skills is not None:
            instance.skills_needed.set(skills)

        if industries is not None:
            instance.industries.set(industries)

        return instance