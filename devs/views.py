from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from devs.serializers import DeveloperWriteSerializer, RegisterSerializer, DeveloperReadSerializer
from rest_framework import viewsets, generics
from devs.models import Developer, User
# from rest_framework.permissions import IsAuthenticatedOrReadOnly



from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token



from rest_framework.response import Response




class DeveloperViewSet(viewsets.ModelViewSet): 
    
    # permission_classes = [IsAuthenticatedOrReadOnly]

    # queryset = DeveloperProfile.objects.all().select_related("user")
    queryset = Developer.objects.all()\
    .select_related("user")\
    .prefetch_related("skills", "industries", "vibes")

    #serializer_class = DeveloperSerializer


    filter_backends = [DjangoFilterBackend, SearchFilter]

    # 🔍 filtering (your UI filters)
    filterset_fields = [
        "city",
        "level",
        "availability",
        "work_preference",
    ]

    # 🔎 search (GitHub-style search bar)
    search_fields = [
        "title",
        "description",
        "user__first_name",
        "user__last_name",
        "about",
        "projects",
    ]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return DeveloperWriteSerializer
        return DeveloperReadSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user) OLD WAY, this would throw an error if a developer profile already exists for the user, which is not ideal since we want to allow users to update their profile without having to delete and recreate it. The new way below checks if a developer profile already exists for the user and reuses it if it does, otherwise it creates a new one. This way we can avoid the error and also allow users to update their profile without having to delete and recreate it.
        
    # def perform_create(self, serializer): # this is where we link the developer profile to the user who created it
    #     user = self.request.user

    #     developer, created = Developer.objects.get_or_create( 
    #         user=user, 
    #         defaults=serializer.validated_data
    #     ) # if a developer profile already exists for this user, silently reuses existing, but it does not update fields

    #     serializer.instance = developer

def perform_create(self, serializer):

    user = self.request.user

    validated_data = serializer.validated_data.copy()

    skills = validated_data.pop("skills", [])

    developer, created = Developer.objects.get_or_create(
        user=user
    )

    for attr, value in validated_data.items():
        setattr(developer, attr, value)

    developer.save()

    developer.skills.set(skills)

    serializer.instance = developer




class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username
            #'email': token.user.email,
        })
    
    # maybe Return user + token shaped like this is better for frontend to use instead of making another request to get user info after login
        # return Response({
        #     "user": {
        #         "id": user.id,
        #         "username": user.username
        #     },
        #     "token": token.key
        # })
 
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        # Create user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create token for that user
        token, created = Token.objects.get_or_create(user=user)

        # Return user + token
        return Response({
            'user_id': token.user_id,
            'username': token.user.username,
            "token": token.key
        })