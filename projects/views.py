from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


from .models import Project
from .serializers import ProjectWriteSerializer, ProjectReadSerializer 

from rest_framework.viewsets import ModelViewSet

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        # Allow read-only requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only owner can edit/delete
        return obj.owner == request.user
    

# class ProjectListView(generics.ListAPIView):
#     queryset = Project.objects.all().select_related("owner")
#     serializer_class = ProjectSerializer

#     filter_backends = [DjangoFilterBackend, SearchFilter]

#     filterset_fields = [
#         "city",
#         "type",
#         "budget",
#         "timeline",
#         "stage",
#     ]

#     search_fields = [
#         "title",
#         "description",
#         "owner__first_name",
#         "owner__last_name",
#     ]


# class ProjectDetailView(generics.RetrieveAPIView):
#     queryset = Project.objects.all().select_related("owner")
#     serializer_class = ProjectSerializer



# --- EXTRA VIEWS FOR FRONTEND FORMS ---
class ProjectViewSet(ModelViewSet):
    # queryset = Project.objects.all()
    queryset = Project.objects.all().select_related("owner").prefetch_related("industries", "skills_needed")
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter]

    # 🔍 filtering (your UI filters)
    filterset_fields = [
        "industries",
        "type",
    ]

    # 🔎 search (GitHub-style search bar)
    search_fields = [
        "title",
        "description",
        "owner__username",   
        "owner__email",      
    ]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProjectWriteSerializer
        return ProjectReadSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)