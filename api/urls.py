from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserRegistrationView,
    HackathonListCreateView,
    HackathonDetailView,
    EnrolledHackathonListView,
    UserSubmissionInView,
    HackathonRegistrationView, HackathonSubmissionView,
)

urlpatterns = [
    # Your other URL patterns
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('hackathons/', HackathonListCreateView.as_view(), name='hackathon-list-create'),
    path('hackathons/<int:pk>/', HackathonDetailView.as_view(), name='hackathon-detail'),
    path('hackathons/register/', HackathonRegistrationView.as_view(), name='hackathon_registration'),
    path('hackathons/<int:pk>/submission/', HackathonSubmissionView.as_view(), name='hackathon_submission'),
    path('registered-hackathons/', EnrolledHackathonListView.as_view(), name='register-hackathon-list'),
    path('registered-hackathons/submission/', UserSubmissionInView.as_view(),name='user-submission-in-hackathon'),

]
