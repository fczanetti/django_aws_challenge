from django.urls import path
from image_upload.base import views


app_name = "base"
urlpatterns = [
    path("", views.home, name="home")
]
