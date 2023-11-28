import os
import uuid
import requests

from django.core.files.uploadedfile import UploadedFile
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status

from image_downloader.models import Image
from imageDownloadService.settings import MEDIA_ROOT
from imageDownloadService import logger


def download_file(url:str, local_file_path:str, local_file_name:str) -> tuple:
    """
    Download a file from the given URL and save it locally.

    Args:
    - url: The URL of the file to be downloaded.
    - local_file_path: The local directory where the file should be saved.

    Returns:
    - tuple: A tuple containing the following elements:
        - str: The full path to the downloaded file on success, or an empty string on failure.
        - bool: True if the file was successfully downloaded and saved, False otherwise.
    """
    raw_data = requests.get(url)
    data = raw_data.content
    content_length = raw_data.headers.get('content-length')
    content_type = raw_data.headers.get('content-type')
    if not content_length or not content_type:
        logger.error(f"Missing content length or content type headers for {url}")
        return "", False

    format = content_type.split("/")[-1]

    file_name = os.path.join(local_file_path, f'{local_file_name}.{format}')
    with open(file_name, 'wb') as fp:
        fp.write(data)
    logger.info(f"File downloaded from {url} and saved as {file_name}")
    return file_name, True


def save_images_data(request) -> list:
    """
    Save image data from the provided source URLs.

    Args:
    - request: The Django request object containing the image source URLs in the 'source_url' field.

    Returns:
    - list: A list of Image instances created and saved in the database.

    This function iterates through the provided image URLs, downloads each image,
    creates corresponding Image model instances, and saves them in the database.
    The local copies of the downloaded images are temporarily stored before
    being associated with the Image instances. Any invalid images are marked as such.
    """
    image_urls = request.data.get('source_url', [])
    file_path = os.path.join(MEDIA_ROOT, 'images')
    image_instaces = []
    user = request.user

    for url in image_urls:
        file_name = str(uuid.uuid4())
        local_file_path, is_valid = download_file(url, file_path, file_name)

        if is_valid:
            try:
                image_object = Image.objects.create(file_name = file_name, source_url = url, user = user)
                image_object.is_valid = True
                image_object.image = UploadedFile(file=open(local_file_path, "rb"))
                image_object.local_file_path = local_file_path
                image_object.save()
                logger.info(f"Image data saved for {url}")
                image_instaces.append(image_object)
            except IntegrityError as e:
                logger.exception(e)
        if local_file_path: os.remove(local_file_path)
    return image_instaces


def list_valid_images():
    """
    Retrieve a queryset of valid Image instances.

    Args:
    - queryset: A queryset of Image instances where 'is_valid' is True.

    This function queries the database to retrieve a list of Image instances
    that are marked as valid ('is_valid' is True). The result is a queryset containing
    Image instances that can be used in your application.
    """
    return Image.objects.filter(is_valid = True)


def exception_handler(func):
    """
    Decorator to handle exceptions.

    Args:
    - func: The function to be wrapped with exception handling.

    Returns:
    - function: A wrapped function that captures and logs any exceptions that occur.
      If an exception is caught, it returns a default error response with a 500 status code.
    """
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(e)
            return Response("something went wrong", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper
