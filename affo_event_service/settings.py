import sys  # noqa

from dynaconf import LazySettings, Validator

settings = LazySettings(ENVVAR_PREFIX_FOR_DYNACONF="AFFO_EV", ENVVAR_FOR_DYNACONF="AFFO_EV_SETTINGS")

# Register validators
settings.validators.register(Validator("CELERY_BROKER_URL", must_exist=True),)

# Fire the validator
settings.validators.validate()

# SECRET CONFIGURATION
SECRET_KEY = getattr(settings, "SECRET_KEY", "")

# CELERY CONFIGURATION
CELERY_BROKER_URL = settings.CELERY_BROKER_URL
CELERY_IMPORTS = ("src.tasks.postback",)

settings.populate_obj(sys.modules[__name__])
