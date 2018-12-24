"""
Transformers for all peer instruction events
"""


def ubc_peer_instruction_original_submitted(current_event, caliper_event):
    """
    The server emits this event when learners submit their initial responses.
    These events records the answer choice the learner selected and the
    explanation given for why that selection was made.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'AssessmentEvent',
        'action': 'Submitted',
        'object': {
            'id': current_event['referer'],
            'type': 'Assessment',
            'extensions': current_event['event']
        }
    })
    caliper_event['extensions']['extra_fields'].update({
        'asides': current_event['context']['asides'],
        'course_id': current_event['context']['course_id'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'module': current_event['context']['module']
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']
    caliper_event['extensions']['extra_fields'].pop('session')
    return caliper_event
