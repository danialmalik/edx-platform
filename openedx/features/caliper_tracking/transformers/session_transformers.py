"""
Transformers for all the session related events.
"""
from django.conf import settings

from openedx.features.caliper_tracking.utils import get_user_link_from_username


def edx_user_login(current_event, caliper_event):
    """
    Server emits this event when user attempts to login.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': settings.LMS_ROOT_URL,
        'type': 'SoftwareApplication',
        'extensions': current_event['event']
    }
    caliper_event.update({
        'action': 'LoggedIn',
        'type': 'SessionEvent',
        'object': caliper_object
    })
    caliper_event['referrer'].update({
        'type': 'WebPage'
    })
    username = current_event['event']['username']
    user_link = get_user_link_from_username(username)
    caliper_event['actor'].update({
        'id': user_link,
        'name': username,
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']
    return caliper_event
