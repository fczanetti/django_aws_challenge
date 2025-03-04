from django.urls import reverse
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile


def test_should_render_form_page(client):
    url = reverse("base:home")

    resp = client.get(url)
    assert resp.status_code == 200


@patch("image_upload.base.views.requests.post")
def test_should_send_request_to_api_gateway(mocked_requests, client, settings):
    api_url = settings.API_GATEWAY_URL
    settings.STORAGES = {"default": {"BACKEND": "django.core.files.storage.InMemoryStorage",}}
    url = reverse("base:home")
    image = SimpleUploadedFile("teste.png", b'image_data', content_type="application/png")
    
    data = {"image": image}
    client.post(url, data)
    
    image.seek(0)
    headers = {"Content-Type": "application/png"}
    mocked_requests.assert_called_once_with(api_url, data=image.read(), headers=headers, params={"filename": image.name})


@patch("image_upload.base.views.log.info")
@patch("image_upload.base.views.requests.post", side_effect=Exception("Any exception"))
def test_should_log_message_when_exception_is_raised(mocked_requests, mocked_log, client, settings):
    settings.STORAGES = {"default": {"BACKEND": "django.core.files.storage.InMemoryStorage",}}
    url = reverse("base:home")
    image = SimpleUploadedFile("teste.png", b'image_data', content_type="application/png")
    
    data = {"image": image}
    client.post(url, data)
    
    mocked_log.assert_called_once_with("An exception was raised when trying to send the image to API-Gateway: Any exception")
