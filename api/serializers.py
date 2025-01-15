from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Family, Individual, Forum, Documentation, Location
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'

class IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = '__all__'

class ForumSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Forum
        fields = '__all__'
        read_only_fields = ('creation_date', 'last_update')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class DocumentationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Documentation
        fields = '__all__'
        read_only_fields = ('upload_date',)
