# Image Download Service

## Task

Implement a web service with a REST interface in Python. The service should offer 3 REST operations.

### 1. Upload a List of Image URLs and Download Corresponding Images

Given a list of image URLs, when the user sends this list to the service via HTTP, the service starts downloading the images. The service puts the images into a persistent storage, allowing them to be listed and retrieved from the service (see operations 2 and 3). There is no need to handle download errors; if a link to the image is incorrect or the image cannot be downloaded, it is simply omitted.

### 2. Get List of Available Images

When the user calls this operation via HTTP, the service replies with a list of all images that were successfully processed through calls to the previous operation (1).

### 3. Retrieve an Image

Given that there were previously images processed via operation 1, when the user calls this operation with a URL as an input parameter, the service sends the corresponding image if it was stored previously through operation 1.

Throughout operations 1 to 3, the key of images should always be the full URL that was used in the original input list for operation 1.

## Implementation Details

### Technologies Used

- Python
- Django (REST framework for handling HTTP requests)
- Persistent Storage (for storing downloaded images)- currently the images are stored locally

### How to Run

1. Clone the repository:

    ```bash
    git clone git@github.com:ArtiSain95/Image-Download.git
    cd Image-Download
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
    
3. Create folder `logs` and `media/images` into the project dir.

4. Run the Django development server:

    ```bash
    python manage.py runserver
    ```

5. The service will be accessible at `http://127.0.0.1:8000/`.


## API Endpoints

### 1. Upload a List of Image URLs

- **Endpoint:** `/image/`
- **Method:** `POST`
- **Request Payload:**
  ```json
  {
    "source_url": ["https://example.com/image1.jpg", "https://example.com/image2.png"]
  }
  ```
### 1. Get List of Available Images
- **Endpoint:** `/image/`
- **Method:** `GET`

### 1. Retrieve an Image
- **Endpoint:** `/images/<image_url>/`
- **Method:** `GET`

