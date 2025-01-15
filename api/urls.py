from django.urls import path
from rest_framework.authtoken import views as token_views
from .views import (
     ProfileAPIView, FamilyListAPIView, FamilyDetailAPIView,
    IndividualListAPIView, IndividualDetailAPIView,
    ForumListAPIView, ForumDetailAPIView,
    DocumentationListAPIView, LocationListAPIView,RegisterAPIView,LoginAPIView,LogoutAPIView
)

urlpatterns = [
    
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('token-auth', token_views.obtain_auth_token, name='api_token_auth'),
    path('profile', ProfileAPIView.as_view(), name='api_profile'),
    path('families', FamilyListAPIView.as_view(), name='api_families'),
    path('families/<int:pk>', FamilyDetailAPIView.as_view(), name='api_family_detail'),
    path('individuals', IndividualListAPIView.as_view(), name='api_individuals'),
    path('individuals/<int:pk>', IndividualDetailAPIView.as_view(), name='api_individual_detail'),
    path('forums', ForumListAPIView.as_view(), name='api_forums'),
    path('forums/<int:pk>', ForumDetailAPIView.as_view(), name='api_forum_detail'),
    path('documentation', DocumentationListAPIView.as_view(), name='api_documentation'),
    path('locations', LocationListAPIView.as_view(), name='api_locations'),
]