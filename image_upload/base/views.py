import requests
import logging
import boto3
from datetime import datetime

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

log = logging.getLogger(__name__)

s3_client = boto3.client(
    "s3", 
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)
bucket_name = settings.AWS_BUCKET_NAME


def home(request):
    filename = "no_file"

    if request.method == "POST":
        url = settings.API_GATEWAY_URL
        image = request.FILES.get("image")
        
        filename = image.name
        filename = f"{datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')}_{filename}"

        image_content = image.read()
        headers = {"Content-Type": "application/png"}
        try:
            requests.post(url, data=image_content, headers=headers, params={"filename": filename})
        except Exception as e:
            log.info(f"An exception was raised when trying to send the image to API-Gateway: {e}")
        
    return render(request, "base/base.html", {"filename": filename})


def get_download_url(request, filename):
    try:
        resp = s3_client.generate_presigned_url(
            'get_object', 
            Params={'Bucket': bucket_name, 'Key': f"resized/{filename}"}, 
            ExpiresIn=3000
        )
    except Exception as e:
        return JsonResponse({}, status=404)
    
    return JsonResponse({"url": resp})
