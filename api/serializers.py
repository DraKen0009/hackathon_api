from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Submission, Hackathon, HackathonRegistration


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True,
            },
            'hackathon': {
                'read_only': True,
            },
        }

    def create(self, validated_data):
        user = self.context['request'].user
        hackathon = validated_data['hackathon']

        # Check if the user is registered for the hackathon
        if not HackathonRegistration.objects.filter(user=user, hackathon=hackathon).exists():
            raise serializers.ValidationError("You are not registered for this hackathon.")

        submission = Submission.objects.create(**validated_data)
        return submission

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        hackathon = instance.hackathon
        submission_type = hackathon.submission_type
        representation['user'] = instance.user.username
        representation['hackathon'] = instance.hackathon.title

        if submission_type == 'image':
            representation.pop('file_submission', None)
            representation.pop('link_submission', None)
        elif submission_type == 'file':
            representation.pop('image_submission', None)
            representation.pop('link_submission', None)
        elif submission_type == 'link':
            representation.pop('image_submission', None)
            representation.pop('file_submission', None)

        return representation

    def validate(self, data):
        hackathon = self.context['view'].get_object()
        submission_type = hackathon.submission_type

        if submission_type == 'image':
            if not data.get('image_submission'):
                raise serializers.ValidationError("Image submission is required.")
            data.pop('file_submission', None)
            data.pop('link_submission', None)
        elif submission_type == 'file':
            if not data.get('file_submission'):
                raise serializers.ValidationError("File submission is required.")
            data.pop('image_submission', None)
            data.pop('link_submission', None)
        elif submission_type == 'link':
            if not data.get('link_submission'):
                raise serializers.ValidationError("Link submission is required.")
            data.pop('image_submission', None)
            data.pop('file_submission', None)

        return data



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class HackathonSerializer(serializers.ModelSerializer):
    submissions = SubmissionSerializer(many=True, read_only=True)
    registrations = serializers.SerializerMethodField()
    submission_count = serializers.SerializerMethodField()

    class Meta:
        model = Hackathon
        fields = '__all__'

    def get_registrations(self, obj):
        return obj.hackathonregistration_set.count()

    def get_submission_count(self, obj):
        user = self.context['request'].user
        return Submission.objects.filter(user=user, hackathon=obj).count()


class HackathonRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonRegistration
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True,
            },
        }
