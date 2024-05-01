import os
import uuid

import aiofiles
from fastapi import HTTPException, File, UploadFile, status as st

from security import check_for_malware
from config import read_config


# The directory where the images for posts are saved (ran when the module is imported from main):
IMAGE_DIRECTORY = read_config("image_directory")

# The image MIME (content) types that are allowed:
IMAGE_MIME_TYPES = read_config("image_mime_types")


async def create_image(image: UploadFile = File(...)) -> str: 
    image_path = ""
    
    # Checking if the uploaded file is of an allowed image type:
    if image.content_type not in IMAGE_MIME_TYPES:
        await image.close()  # Close the file to clean up resources
        raise HTTPException(status_code=st.HTTP_400_BAD_REQUEST, detail="Unsupported file type")

    # Generating a universally unique ID for the image file name:
    image_uuid = uuid.uuid4()

    # os.path.splittext splits the string into two parts (before and after the last dot):
    extension = os.path.splitext(image.filename)[1]
    image_path = os.path.join(IMAGE_DIRECTORY, f"{image_uuid}{extension}")

    try:    
        # Checking for malware in the image file:
        check_for_malware(image)

        # "wb" is for writing in binary mode, aiofiles allows async operations:
        async with aiofiles.open(image_path, "wb") as saved_image:
            # await is used to not block the event loop when calling async functions:
            content = await image.read()
            await saved_image.write(content)

        return image_path
    
    except Exception as e:
        print(f"Error saving image: {e}")

        # Deleting the image file if it exists:
        if os.path.exists(image_path): os.remove(image_path)

        # Commits and rollbacks are handled in the context manager.
        # Raising the exception again to be caught by the exception handler (HTTP Exception returned to the client):
        raise e

    finally:
        await image.close()