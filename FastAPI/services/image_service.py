import os
import uuid
from PIL import Image, ImageOps

from fastapi import File, UploadFile

from security import check_for_malware
from config import read_config
from exceptions import UnsupportedFileTypeError, UnableToProcessInputError

# The directory where the images for posts are saved (ran when the module is imported from main):
IMAGE_DIRECTORY = read_config("image_directory")

# The image MIME (content) types that are allowed:
IMAGE_MIME_TYPES = read_config("image_mime_types")

# Maximum dimension for compressed images:
COMPRESSION_DIMENSION = read_config("compression_size")


def save_file(upload_file: UploadFile) -> str:
    # Generating a unique filename for the uploaded file:
    file_uuid = uuid.uuid4()
    file_url = os.path.join(IMAGE_DIRECTORY, f"{file_uuid}{os.path.splitext(upload_file.filename)[1]}")

    with open(file_url, "wb") as file_object:
        file_object.write(upload_file.file.read())

    return file_url


def compress_image(url: str) -> str:
    img = Image.open(url)
    
    # Automatically correcting the orientation from EXIF data:
    img = ImageOps.exif_transpose(img)
    
    # Resizing the image while preserving the aspect ratio:
    img.thumbnail((COMPRESSION_DIMENSION, COMPRESSION_DIMENSION))
    
    img.save(url, optimize=True)

    return url


async def create_image(image: UploadFile = File(...)) -> str: 
    
    try:    
        # Checking if the uploaded file is of an allowed image type:
        if image.content_type not in IMAGE_MIME_TYPES:
            raise UnsupportedFileTypeError()

        # Saving the image:
        url = save_file(image)

        # Checking for malware in the image file:
        check_for_malware(image)

        # Compressing the image:
        url = compress_image(url)

        return url
    
    except Exception as e:
        print(f"Error occurred: {e}")

        raise UnableToProcessInputError() from e