import io
from PIL import Image
import pytest


@pytest.fixture
def django_image_file(tmp_path):
    """Фабрика изображений: django_image_file(name, size=(100,100)) -> InMemoryUploadedFile"""

    def _make(name: str, size=(100, 100), color=(155, 0, 0)):
        from django.core.files.uploadedfile import SimpleUploadedFile

        img = Image.new("RGB", size, color=color)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)
        return SimpleUploadedFile(name, buf.read(), content_type="image/jpeg")

    return _make
