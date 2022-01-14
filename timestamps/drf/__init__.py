def __require_djangorestframework():
    try:
        import rest_framework
    except ImportError as e:
        raise ImportError(
                'djangorestframework not installed. '
                'run `pip install django-timestampable[drf]` '
                'and add "rest_framework" to your INSTALLED_APPS') \
            from e


__require_djangorestframework()
