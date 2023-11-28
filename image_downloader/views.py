from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

from image_downloader.models import Image
from imageDownloadService import logger
from django.shortcuts import get_object_or_404
from django.http.response import Http404 as _http_404_exception
from image_downloader.helpers import save_images_data, list_valid_images, exception_handler
from image_downloader.serializers import ImageSerializer


class ImageAPIView(APIView):
    """
    API View for managing images.
    """

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @exception_handler
    def get(self, request, url=None, format=None):
        """
        API View for retrieving images based on the provided URL or listing all available images.

        - If a specific 'url' parameter is provided, retrieves the corresponding image.
        - If 'url' is not provided, returns a list of all available image URLs.

        Args:
        - request: The Django request object.
        - url: The URL parameter for retrieving a specific image (optional).

        Returns:
        - Response: A JSON response containing the image data or a list of image URLs.

        Raises:
        - Http404: If the requested image URL is not found.
        """
        try:
            url = request.GET.get("url")
            if url is not None:
                data = get_object_or_404(Image, source_url=url)
                serializer = ImageSerializer(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            image_queryset = list_valid_images()
            serializer = ImageSerializer(image_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except _http_404_exception as e:
            logger.exception(e)
            return Response([], status=status.HTTP_404_NOT_FOUND)

    @exception_handler
    def post(self, request, format=None):
        """
        Upload and save images using the provided URLs.

        Args:
        - request: The Django request object.
        - format: The requested format for the response (optional).

        Returns:
        - Response: A JSON response containing the data of the uploaded images.

        The method expects a list of image URLs in the request data and saves them as
        Image instances. It returns a JSON response with the data of the uploaded images.
        """
        image_instances = save_images_data(request)
        serializer = ImageSerializer(image_instances, many = True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
