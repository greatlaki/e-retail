from django.urls import path
from users.views import LoginApiView, LogoutAPIView

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
