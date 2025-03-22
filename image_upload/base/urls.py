from django.urls import path
from image_upload.base import views


app_name = "base"
urlpatterns = [
    path("", views.home, name="home"),
    path("get_download_url/<str:filename>", views.get_download_url, name="download_url")
]
