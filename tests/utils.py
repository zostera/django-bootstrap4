from django import get_version

DJANGO3 = get_version() >= "3"


def html_39x27(html):
    """
    Return HTML string with &#39; (Django < 3) instead of &#x27; (Django >= 3).

    See https://docs.djangoproject.com/en/dev/releases/3.0/#miscellaneous
    """
    if not DJANGO3:
        return html.replace("&#x27;", "&#39;")
    return html
