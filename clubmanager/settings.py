import os


def to_bool(setting):
    if setting == 'True':
        return True
    elif setting is True:
        return True

    return False

is_development = os.getenv("DEVELOPMENT", False)
if to_bool(is_development):
    from .settings_development import *
else:
    from .settings_production import *
