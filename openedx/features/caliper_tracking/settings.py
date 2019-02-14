"""
All settings for Caliper Tracking app.
"""

LOGIN_EVENT_EMITTER = 'openedx.features.caliper_tracking.helpers.emit_login_event'
CALIPER_TRACKING_PROCESSOR = 'openedx.features.caliper_tracking.processor.CaliperProcessor'

CALIPER_TRACKING_BACKENDS = {
    'logger': {
        'ENGINE': CALIPER_TRACKING_PROCESSOR,
        'OPTIONS': {
            'name': 'tracking'
        }
    }
}
