import io
from typing import Any

from ._utils import numpy_available, opencv_available, pillow_available, raise_missing_image_library, raise_missing_numpy_library


def load_file(path: str) -> Any:
    """
    Loads the image from the path.

    :param path: the path to load the image from
    :type path: str
    :return: the image
    """
    if opencv_available():
        import cv2
        return cv2.imread(path)

    if pillow_available():
        from PIL import Image
        return Image.open(path)

    raise_missing_image_library()


def load_bytes(data: bytes) -> Any:
    """
    Loads the image from the bytes.

    :param data: the bytes data to load the image from
    :type data: bytes
    :return: the image
    """
    if opencv_available():
        if not numpy_available():
            raise_missing_numpy_library()
        import cv2
        return cv2.imread(path)

    if pillow_available():
        from PIL import Image
        return Image.open(io.BytesIO(data))

    raise_missing_image_library()


def save_file(img: Any, path: str, jpeg_quality: int = 90):
    """
    Saves the image to the specified file.

    :param img: the image to save
    :param path: the path to save the image to
    :type path: str
    :param jpeg_quality: the quality to use for JPEG files
    :type jpeg_quality: int
    """
    is_jpeg = path.lower().endswith(".jpg") or path.lower().endswith(".jpeg")

    if pillow_available():
        from PIL import Image
        if is_jpeg:
            img.save(path, quality=jpeg_quality)
        else:
            img.save(path)
        return

    if opencv_available():
        import cv2
        if is_jpeg:
            cv2.imwrite(path, img, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality])
        else:
            cv2.imwrite(path, img)
        return

    raise_missing_image_library()


def save_bytes(img: Any, image_format: str, jpeg_quality: int = 90) -> bytes:
    """
    Turns the image into bytes.

    :param img: the image to save
    :param image_format: the format to use, e.g., JPEG or PNG
    :type image_format: str
    :param jpeg_quality: the quality to use for JPEG files
    :type jpeg_quality: int
    :return: the generated bytes structure
    :rtype: bytes
    """
    if image_format.lower() == "jpg":
        image_format = "JPEG"
    is_jpeg = (image_format.lower == "jpeg")

    if pillow_available():
        from PIL import Image
        img_bytes = io.BytesIO()
        if is_jpeg:
            img.save(img_bytes, format=image_format, quality=jpeg_quality)
        else:
            img.save(img_bytes, format=image_format)
        return img_bytes.getvalue()

    if opencv_available():
        import cv2
        if is_jpeg:
            retval, buffer = cv2.imencode(".jpg", img)
        else:
            retval, buffer = cv2.imencode("." + image_format.lower(), img)
        return buffer.tobytes()

    raise_missing_image_library()
