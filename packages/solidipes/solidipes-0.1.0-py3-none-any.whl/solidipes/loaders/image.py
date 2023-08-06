from PIL import Image as PILImage

from .. import viewers
from .file import File


class Image(File):
    """Image loaded with PIL"""

    supported_mime_types = ["image/"]

    def __init__(self, path):
        super().__init__(path)

        self.add("image")
        self.default_viewer = viewers.Image

    def _load_data(self, key):
        """Load image data with PIL"""
        return PILImage.open(self.file_info.path)
