from django.urls import path , include
from .views import login_page , logout_view , register

app_name = 'users'

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('auth/', include('social_django.urls', namespace='social')),
]