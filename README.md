# AWS Challenge

This is the "Django part" of the AWS Challenge completed. It consists in a simple page with a form where you can attach an image and, after sending, this image goes through a flow where it is stored in S3 and processed by a Lambda that adjusts the image size. At the end, the link to download the image is made available on the same page.

The complete flow and details are better described on [this repository](https://github.com/fczanetti/aws_challenge).

To run this project, simply create a new use the commands bellow from the root of the project:

```
cp contrib/env-sample .env
python -m venv .venv
source .venv/bin/activate
python manage.py migrate
python manage.py runserver
```

This should be enough to run the single page in `http://127.0.0.1:8000`.