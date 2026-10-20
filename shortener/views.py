
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import ShortURL


def home(request):
    """Display the home page and handle URL shortening requests."""

    if request.method == "POST":
        original_url = request.POST.get("original_url", "").strip()

        try:
            short_url = ShortURL(original_url=original_url)
            short_url.save()

            # Store the result temporarily in the user's session.
            request.session["short_url_id"] = short_url.pk

            # Redirect after POST to prevent accidental resubmission.
            return redirect("home")

        except ValidationError as error:
            return render(
                request,
                "shortener/home.html",
                {
                    "errors": error.messages,
                    "submitted_url": original_url,
                },
            )

    # Retrieve and remove the one-time result from the session.
    short_url_id = request.session.pop("short_url_id", None)
    short_url = None

    if short_url_id is not None:
        short_url = ShortURL.objects.filter(
            pk=short_url_id
        ).first()

    return render(
        request,
        "shortener/home.html",
        {"short_url": short_url},
    )


def redirect_to_original(request, short_code):
    """Redirect the visitor to the original destination URL."""

    try:
        short_url = ShortURL.objects.get(short_code=short_code)
    except ShortURL.DoesNotExist:
        raise Http404("Short URL not found.")

    short_url.register_click()

    return HttpResponseRedirect(short_url.original_url)