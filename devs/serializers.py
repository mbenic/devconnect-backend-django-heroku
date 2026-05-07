
# from rest_framework import serializers
# from .models import (
#     Developer,
#     Skill,
#     Industry,
#     Vibe,
#     City,
#     Level,
#     Availability,
#     WorkPreference,
# )

# class SkillSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Skill
#         fields = ["id", "name"]


# class IndustrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Industry
#         fields = ["id", "name"]


# class VibeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vibe
#         fields = ["id", "name"]



# class DeveloperSerializer(serializers.ModelSerializer):
#     skills = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=Skill.objects.all()
#     )
#     industries = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=Industry.objects.all()
#     )
#     vibes = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=Vibe.objects.all()
#     )

#     class Meta:
#         model = Developer
#         fields = [
#             "id",
#             "name",
#             "email",
#             "about",
#             "portfolio",
#             "linkedin",
#             "github",
#             "city",
#             "level",
#             "availability",
#             "work_preference",
#             "projects",
#             "skills",
#             "industries",
#             "vibes",
#         ]

from rest_framework import serializers
from .models import ( Developer, Skill, Industry, Vibe , User)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class SkillGroupedSerializer(serializers.Serializer):
    label = serializers.CharField()
    skills = serializers.ListField(child=serializers.CharField())
    #skills = SkillSerializer(many=True, read_only=True)



class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ["id", "name"]


class VibeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vibe
        fields = ["id", "name"]



class DeveloperSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    skills = serializers.SerializerMethodField()
    industries = serializers.SerializerMethodField()
    vibes = serializers.SerializerMethodField()

    links = serializers.SerializerMethodField()

    class Meta:
        model = Developer
        fields = [
            "id",
            "name",
            "email",
            "city",
            "level",
            "about",
            "availability",
            "work_preference",
            "skills",
            "industries",
            "vibes",
            "links",
            "projects",
            "created_at",
        ]

    # 👇 flatten user
    def get_name(self, obj):
        return obj.user.get_full_name()

    def get_email(self, obj):
        return obj.user.email

    # 👇 convert M2M → string arrays
    def get_skills(self, obj):
        return [s.name for s in obj.skills.all()]

    def get_industries(self, obj):
        return [i.name for i in obj.industries.all()]

    def get_vibes(self, obj):
        return [v.name for v in obj.vibes.all()]

    # 👇 nested links object (IMPORTANT)
    def get_links(self, obj):
        return {
            "portfolio": obj.portfolio,
            "linkedin": obj.linkedin,
            "github": obj.github,
        }
    
    
class DeveloperWriteSerializer(serializers.ModelSerializer):
        skills = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Skill.objects.all()
        )
        industries = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=Industry.objects.all()
        )
        vibes= serializers.PrimaryKeyRelatedField(
            many=True,  
            queryset=Vibe.objects.all()
        )
        class Meta:
            model = Developer
            fields = [
                
                "city",
                "level",
                "about",
                "projects",
                "availability",
                "work_preference",
                "portfolio",
                "linkedin",
                "github",
                "skills",
                "industries",
                "vibes",
            ]


class DeveloperReadSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    # nested relations
    skills = SkillSerializer(many=True)
    industries = IndustrySerializer(many=True)
    vibes = VibeSerializer(many=True)

    # choice labels
    level_display = serializers.CharField(source="get_level_display")
    availability_display = serializers.CharField(source="get_availability_display")
    work_preference_display = serializers.CharField(source="get_work_preference_display")
    city_display = serializers.CharField(source="get_city_display")
    

    class Meta:
        model = Developer
        fields = [
            "id",
            "name",
            "email",
            "city",
            "city_display",
            "level",
            "level_display",
            "about",
            "projects",
            "availability",
            "availability_display",
            "work_preference",
            "work_preference_display",
            "links",
            "skills",
            "industries",
            "vibes",
            "created_at"

        ]
# 👇 flatten user
    def get_name(self, obj):
        return obj.user.get_full_name()

    def get_email(self, obj):
        return obj.user.email

    # # 👇 convert M2M → string arrays
    # def get_skills(self, obj):
    #     return [s.name for s in obj.skills.all()]

    # def get_industries(self, obj):
    #     return [i.name for i in obj.industries.all()]

    # def get_vibes(self, obj):
    #     return [v.name for v in obj.vibes.all()]

    # 👇 nested links object (IMPORTANT)
    def get_links(self, obj):
        return {
            "portfolio": obj.portfolio,
            "linkedin": obj.linkedin,
            "github": obj.github,
        }