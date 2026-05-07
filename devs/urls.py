# from django.urls import path
# from .views import DeveloperListView, DeveloperDetailView 

# urlpatterns = [

#     path("", DeveloperListView.as_view(), name="dev-list"),
#     path("<int:pk>/", DeveloperDetailView.as_view(), name="dev-detail"),

# ]

# from django.urls import path
# from rest_framework.routers import DefaultRouter
# from .views import DeveloperViewSet, CustomAuthToken, RegisterView

# router = DefaultRouter()
# router.register(r"", DeveloperViewSet, basename="devs")

# urlpatterns = [
#     path("register/", RegisterView.as_view()),
#     path("login/", CustomAuthToken.as_view()),
# ]

# urlpatterns += router.urls

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import DeveloperViewSet, CustomAuthToken, RegisterView

# router = DefaultRouter()
# router.register(r"devs", DeveloperViewSet, basename="devs")

# urlpatterns = [
#     path("register/", RegisterView.as_view()),
#     path("login/", CustomAuthToken.as_view()),
#     path("", include(router.urls)),
# ]

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import DeveloperViewSet, CustomAuthToken, RegisterView

router = SimpleRouter()
router.register(r"", DeveloperViewSet, basename="devs")

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", CustomAuthToken.as_view()),
    path("", include(router.urls)),
]

