
from django.apps import AppConfig
from django.conf import settings


LOGIN_EVENT_EMITTER = 'caliper_tracking.helpers.emit_login_event'


class CaliperTrackingConfig(AppConfig):
    name = 'openedx.features.caliper_tracking'
    verbose_name = "Caliper Tracking"

    def ready(self):
        # To override the settings after third_party_auth.
        if settings.FEATURES.get('ENABLE_THIRD_PARTY_AUTH'):
            self._apply_third_party_auth_settings()

    def _apply_third_party_auth_settings(self):
        """
        Apply the settings for third party auth app.
        """
        settings.SOCIAL_AUTH_PIPELINE.append(LOGIN_EVENT_EMITTER)
