"""
Shared model mixins for the Brauni project.
"""

import os

from django.core.files.base import ContentFile
from django.templatetags.static import static

from apps.admin_utils import compress_image


class ImageURLMixin:
    """
    Adds an ``image_url`` property and automatic WebP compression on save
    for the field named by ``image_field_name`` (default ``"image"``).

    Falls back to the project placeholder when no image is set.

    Models with multiple image fields (e.g. HomeBlock) should set
    ``image_field_name`` to the primary display field and override
    ``save()`` to compress all image fields.
    """

    image_field_name: str = "image"

    @property
    def image_url(self) -> str:
        image = getattr(self, self.image_field_name, None)
        if image:
            try:
                return image.url
            except ValueError:
                pass
        return static("images/placeholders/placeholder.png")

    def save(self, *args, **kwargs):
        self._compress_image_field(self.image_field_name)
        super().save(*args, **kwargs)

    def _compress_image_field(self, field_name: str):
        """Compress a single image field to WebP on first save."""
        image_field = getattr(self, field_name, None)

        if not image_field or not hasattr(image_field, "file"):
            return

        flag_attr = f"_image_compressed_{field_name}"
        if getattr(self, flag_attr, False):
            return

        try:
            original_name = image_field.name
            compressed_stream = compress_image(image_field)

            base, _ = os.path.splitext(original_name)
            new_name = f"{base}.webp"

            image_field.save(
                new_name,
                ContentFile(compressed_stream.read()),
                save=False,
            )

            setattr(self, flag_attr, True)
        except Exception:
            # If compression fails, keep original image as-is
            pass
