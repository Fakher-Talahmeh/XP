from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from .models import Family, Individual, Forum, Documentation, Location,Profile
from .serializers import (
    FamilySerializer, IndividualSerializer, ForumSerializer,
    DocumentationSerializer, LocationSerializer, ProfileSerializer,RegisterSerializer, LoginSerializer)
from django.contrib.auth import login, logout, authenticate
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                token, created = Token.objects.get_or_create(user=user)
                request.session['auth_token'] = token.key
                login(request, user) 
                return Response({
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name
                    },
                    "token": token.key,
                    "message": "Login successful",
                }, status=200)
            return Response({
                "message": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token, created = Token.objects.get_or_create(user=user)
                request.session['auth_token'] = token.key
                login(request, user)  
                Profile.objects.create(user=user)
                return Response({
                    "user": serializer.data,
                    "token": token.key,
                    "message": "User created successfully"
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self, request):
        try:
            if 'auth_token' in request.session:
                del request.session['auth_token']
            
            request.user.auth_token.delete()
            
            logout(request)
            
            return Response({
                "message": "Successfully logged out."
            })
        except Exception as e:
            return Response({
                "message": "Error logging out",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(request.user.profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FamilyListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        families = Family.objects.all()
        serializer = FamilySerializer(families, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FamilySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FamilyDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Family, pk=pk)

    def get(self, request, pk):
        family = self.get_object(pk)
        serializer = FamilySerializer(family)
        return Response(serializer.data)

    def put(self, request, pk):
        family = self.get_object(pk)
        serializer = FamilySerializer(family, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        family = self.get_object(pk)
        family.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class IndividualListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        individuals = Individual.objects.all()
        serializer = IndividualSerializer(individuals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IndividualSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IndividualDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Individual, pk=pk)

    def get(self, request, pk):
        individual = self.get_object(pk)
        serializer = IndividualSerializer(individual)
        return Response(serializer.data)

    def put(self, request, pk):
        individual = self.get_object(pk)
        serializer = IndividualSerializer(individual, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        individual = self.get_object(pk)
        individual.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ForumListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        forums = Forum.objects.all()
        serializer = ForumSerializer(forums, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ForumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForumDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Forum, pk=pk)

    def get(self, request, pk):
        forum = self.get_object(pk)
        serializer = ForumSerializer(forum)
        return Response(serializer.data)

    def put(self, request, pk):
        forum = self.get_object(pk)
        if forum.user != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ForumSerializer(forum, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        forum = self.get_object(pk)
        if forum.user != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        forum.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DocumentationListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        docs = Documentation.objects.all()
        serializer = DocumentationSerializer(docs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocationListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
