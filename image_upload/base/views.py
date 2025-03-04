from django.shortcuts import render
import requests
import logging

from django.conf import settings

log = logging.getLogger(__name__)


def home(request):
    if request.method == "POST":
        url = settings.API_GATEWAY_URL
        image = request.FILES.get("image")
        filename = image.name
        image_content = image.read()
        headers = {"Content-Type": "application/png"}
        try:
            requests.post(url, data=image_content, headers=headers, params={"filename": filename})
        except Exception as e:
            log.info(f"An exception was raised when trying to send the image to API-Gateway: {e}")
        

    return render(request, "base/base.html", {})
