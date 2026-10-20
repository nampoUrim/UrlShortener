
import re
import secrets
import string
from urllib.parse import urlparse
from django.db.models import F
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models


def validate_http_https_url(value):
    """Ensure that the URL uses HTTP or HTTPS and has a network location."""

    # Allow only HTTP and HTTPS protocols.
    validator = URLValidator(schemes=["http", "https"])
    validator(value)

    # Parse the URL to inspect its components.
    parsed_url = urlparse(value)

    # Ensure that the URL contains a domain or network location.
    if not parsed_url.netloc:
        raise ValidationError(
            "The URL must contain a valid domain."
        )


def validate_short_code(value):
    """Ensure that the short code contains exactly six alphanumeric characters."""

    # Accept only uppercase letters, lowercase letters, and digits.
    if not re.fullmatch(r"[A-Za-z0-9]{6}", value):
        raise ValidationError(
            "The short code must contain exactly "
            "6 alphanumeric characters."
        )


def generate_short_code():
    """Generate a unique, random six-character short code."""

    # Combine uppercase letters, lowercase letters, and digits.
    alphabet = string.ascii_letters + string.digits

    while True:
        # Generate a random code containing six characters.
        short_code = "".join(
            secrets.choice(alphabet)
            for _ in range(6)
        )

        # Return the code only if it is not already in use.
        if not ShortURL.objects.filter(
            short_code=short_code
        ).exists():
            return short_code


class ShortURL(models.Model):
    # Store the original destination URL.
    original_url = models.URLField(
        validators=[validate_http_https_url],
    )

    # Store a unique, six-character code for the shortened URL.
    # blank=True allows the code to be omitted from forms and validation;
    # save() generates it automatically when it is missing.
    short_code = models.CharField(
        max_length=6,
        unique=True,
        validators=[validate_short_code],
        blank=True,
    )

    # Automatically record the date and time when the link is created.
    created_at = models.DateTimeField(auto_now_add=True)

    # Count the number of recorded clicks, starting at zero.
    click_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """Generate a missing code, validate the object, and save it."""

        # Generate a code if none has been provided.
        if not self.short_code:
            self.short_code = generate_short_code()

        # Validate the fields and model constraints before saving.
        self.full_clean()

        # Call Django's original save method to persist the object.
        super().save(*args, **kwargs)

    def get_short_path(self):
        """Return the relative path associated with this short code."""

        return f"/{self.short_code}/"

    def register_click(self):
        """Increment the click counter safely under concurrent requests."""

        ShortURL.objects.filter(pk=self.pk).update(
            click_count=F("click_count") + 1
        )

    # Refresh the local object with the updated database value.
        self.refresh_from_db(fields=["click_count"])

    def __str__(self):
        """Return the short code as the object's text representation."""

        return self.short_code
