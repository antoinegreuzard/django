"""
Context processors for the app.

This module contains context processors that add custom context variables to
the context of all templates rendered using Django's RequestContext.
"""


def site_name(request):
    """
    Adds a 'SITE_NAME' variable to the context.

    This can be used in templates to dynamically insert the name of the site.

    Args:
        request: The HttpRequest object.

    Returns:
        A dictionary containing the 'SITE_NAME' context variable.
    """
    return {'SITE_NAME': ' - Ma Bibliothèque'}
