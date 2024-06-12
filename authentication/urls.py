# urls.py
from django.urls import path
from .views import login_view, sign_up_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', sign_up_view, name='sign_up'),
]
