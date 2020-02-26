from django.urls import path
from user_api import views

app_name = 'user_api'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('update/', views.RetrieveUpdateUserView.as_view(), name='update'),
    path('deactivate/', views.DeactivateUserView.as_view(), name='Deactivate'),

    path('token/', views.CreateTokenView.as_view(), name='token'),
]
