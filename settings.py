# Settings for this app.

settings = dict(
# the main settings dict contains nothing right now.
# we use this to get secret things from settings_local
)

try:
    # pull in settings_local if it exists
    from settings_local import settings as s
    settings.update(s)
except ImportError:
    pass
