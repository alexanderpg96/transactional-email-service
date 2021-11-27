"""emailservice urls."""
from django.urls import path
from api import views

urlpatterns = [path("email", views.EmailMessageView.as_view())]
