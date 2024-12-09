import os
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
import yt_dlp

# Django settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DEBUG=True,
    SECRET_KEY='your-secret-key',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    INSTALLED_APPS=['django.contrib.staticfiles'],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
        }
    ],
    STATIC_URL='/static/',
    STATICFILES_DIRS=[os.path.join(BASE_DIR, 'static')],
)

# HTML template for the app
TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            text-align: center;
            background: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        form {
            margin-top: 20px;
        }
        .btn {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px;
        }
        .btn:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>YouTube Video Downloader</h1>
        <form method="post">
            <input type="url" name="video_url" placeholder="Enter YouTube Video URL" required style="width: 80%; padding: 10px;">
            <br><br>
            <button type="submit" class="btn">Download</button>
        </form>
    </div>
</body>
</html>
"""

# View function
def index(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(BASE_DIR, 'downloads/%(title)s.%(ext)s'),
        }
        try:
            if not os.path.exists('downloads'):
                os.makedirs('downloads')

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            return HttpResponse("Download successful! Check the 'downloads' folder.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    return HttpResponse(TEMPLATE_HTML)

# URL patterns
urlpatterns = [
    path('', index),
]

# Run the server
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__main__')
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
