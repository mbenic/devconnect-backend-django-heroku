# from django.urls import path
# from .views import ProjectListView, ProjectDetailView

# urlpatterns = [
#     path("", ProjectListView.as_view(), name="project-list"),
#     path("<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
#     # path("choices/", ProjectChoicesView.as_view(), name="project-choices"),
# ]

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ProjectViewSet

# router = DefaultRouter()
# router.register(r"projects", ProjectViewSet, basename="projects")

# urlpatterns = [
#     path("", include(router.urls)),
# ]


from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ProjectViewSet

router = SimpleRouter()
router.register(r"", ProjectViewSet, basename="projects")

urlpatterns = [
    path("", include(router.urls)),
]