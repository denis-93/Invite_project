from django.urls import path
from .views import AuthorizationView, AuthorizationWithCodeView, ProfileView

app_name = 'api'

urlpatterns = [
    path('authorization/', AuthorizationView.as_view()),
    path('confirm/', AuthorizationWithCodeView.as_view()),
    path('profile/', ProfileView.as_view()),
]
