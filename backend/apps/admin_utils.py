import io

from PIL import Image as PILImage

from django.contrib import messages
from django.db import models
from django.forms import Textarea
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.core.exceptions import ValidationError


CYRILLIC_TRANSLITERATION = str.maketrans(
    {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "c",
        "ч": "ch",
        "ш": "sh",
        "щ": "sch",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
    }
)


def russian_slugify(value):
    return slugify(str(value).lower().translate(CYRILLIC_TRANSLITERATION))


def make_unique_slug(model, value, instance_pk=None):
    base_slug = russian_slugify(value) or "item"
    slug = base_slug
    index = 2
    queryset = model._default_manager.all()

    if instance_pk:
        queryset = queryset.exclude(pk=instance_pk)

    while queryset.filter(slug=slug).exists():
        slug = f"{base_slug}-{index}"
        index += 1

    return slug


def image_preview(obj, field_name="image", width=104, height=72):
    image = getattr(obj, field_name, None)

    if not image:
        return mark_safe('<span class="bf-muted">Нет изображения</span>')

    try:
        url = image.url
    except ValueError:
        return mark_safe('<span class="bf-muted">Нет изображения</span>')

    return format_html(
        '<img src="{}" class="bf-thumb" width="{}" height="{}" loading="lazy" alt="">',
        url,
        width,
        height,
    )


def badge(text, kind="neutral"):
    return format_html('<span class="bf-badge bf-badge--{}">{}</span>', kind, text)


def boolean_badge(value, yes="Активно", no="Отключено"):
    return badge(yes, "success") if value else badge(no, "muted")


def message_for_update(modeladmin, request, updated, action):
    modeladmin.message_user(
        request,
        f"{updated} записей: {action}.",
        messages.SUCCESS,
    )


class ContentTextareaMixin:
    """Shared formfield override — renders all TextField widgets with a compact
    ``rows=5`` textarea so admin forms stay tidy."""

    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 5}),
        },
    }


def validate_image(image):

    max_size_mb = 8

    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Максимальный размер изображения: {max_size_mb}MB")

    valid_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    )

    file_name = image.name.lower()

    if not file_name.endswith(valid_extensions):
        raise ValidationError("Поддерживаются только JPG, PNG и WEBP")


def compress_image(image_file, max_width=2000, quality=82):
    """
    Resize image to *max_width* (keep aspect ratio) and convert to WebP.

    Returns an in-memory BytesIO stream so the original uploaded file can be
    replaced before saving.
    """

    pil = PILImage.open(image_file)

    if pil.mode in ("RGBA", "LA", "P"):
        if pil.mode == "P":
            pil = pil.convert("RGBA")
        elif pil.mode != "RGBA":
            pil = pil.convert("RGBA")

    if pil.mode == "RGBA":
        # Drop alpha channel if it's fully opaque (produces smaller WebP)
        if pil.getchannel("A").getextrema()[0] == 255:
            pil = pil.convert("RGB")

    # Resize if wider than max_width
    if pil.width > max_width:
        ratio = max_width / pil.width
        new_height = int(pil.height * ratio)
        pil = pil.resize((max_width, new_height), PILImage.LANCZOS)

    # Save to in-memory buffer as WebP
    out = io.BytesIO()
    save_kwargs = {"quality": quality, "optimize": True}
    if pil.mode == "RGBA":
        pil.save(out, "WEBP", **save_kwargs, lossless=False)
    else:
        pil.save(out, "WEBP", **save_kwargs)

    out.seek(0)
    return out
