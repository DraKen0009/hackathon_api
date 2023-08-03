from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Submission, Hackathon, HackathonRegistration
from .serializers import UserRegistrationSerializer, SubmissionSerializer, HackathonSerializer, \
    HackathonRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class HackathonListCreateView(generics.ListCreateAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class HackathonDetailView(generics.RetrieveAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
    permission_classes = [IsAuthenticated]


class EnrolledHackathonListView(generics.ListAPIView):
    serializer_class = HackathonSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        enrollments = HackathonRegistration.objects.filter(user=user)
        return [enrollment.hackathon for enrollment in enrollments]


class UserSubmissionInView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        return Submission.objects.filter(user=user)


class HackathonRegistrationView(generics.CreateAPIView):
    queryset = HackathonRegistration.objects.all()
    serializer_class = HackathonRegistrationSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        hackathon_id=request.data['hackathon']
        hackathon=Hackathon.objects.filter(id=hackathon_id).first()
        user=self.request.user
        if HackathonRegistration.objects.filter(user=user, hackathon=hackathon).exists():
            return Response({"detail": "You are Already registered for this hackathon."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, hackathon=hackathon)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj

class HackathonSubmissionView(generics.CreateAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        hackathon = self.get_object()
        user = self.request.user

        if Submission.objects.filter(user=user, hackathon=hackathon).exists():
            return Response({"detail": "You have already submitted your response for this hackathon."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, hackathon=hackathon)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

