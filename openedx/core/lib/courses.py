"""
Common utility functions related to courses.
"""
from django import forms
from django.conf import settings

from opaque_keys import InvalidKeyError
from opaque_keys.edx.locator import CourseKey
from six import text_type
from xmodule.assetstore.assetmgr import AssetManager
from xmodule.contentstore.content import StaticContent
from xmodule.contentstore.django import contentstore
from xmodule.exceptions import NotFoundError
from xmodule.modulestore.django import modulestore


def course_image_url(course, image_key='course_image'):
    """Try to look up the image url for the course.  If it's not found,
    log an error and return the dead link.
    image_key can be one of the three: 'course_image', 'hero_image', 'thumbnail_image' """
    if course.static_asset_path:
        # If we are a static course with the image_key attribute
        # set different than the default, return that path so that
        # courses can use custom course image paths, otherwise just
        # return the default static path.
        url = '/static/' + (course.static_asset_path or getattr(course, 'data_dir', ''))
        if hasattr(course, image_key) and getattr(course, image_key) != course.fields[image_key].default:
            url += '/' + getattr(course, image_key)
        else:
            url += '/images/' + image_key + '.jpg'
    elif not getattr(course, image_key):
        # if image_key is empty, use the default image url from settings
        url = settings.STATIC_URL + settings.DEFAULT_COURSE_ABOUT_IMAGE_URL
    else:
        loc = StaticContent.compute_location(course.id, getattr(course, image_key))
        try:
            AssetManager.find(loc)
        except NotFoundError:
            url = '/static/' + settings.DEFAULT_COURSE_ABOUT_IMAGE_URL
        else:
            url = StaticContent.serialize_asset_key_with_slash(loc)
    return url


def create_course_image_thumbnail(course, dimensions):
    """Create a course image thumbnail and return the URL.

    - dimensions is a tuple of (width, height)
    """
    course_image_asset_key = StaticContent.compute_location(course.id, course.course_image)
    course_image = AssetManager.find(course_image_asset_key)  # a StaticContent obj

    _content, thumb_loc = contentstore().generate_thumbnail(course_image, dimensions=dimensions)

    return StaticContent.serialize_asset_key_with_slash(thumb_loc)


def clean_course_id(model_form, is_required=True):
    """
    Cleans and validates a course_id for use with a Django ModelForm.

    Arguments:
        model_form (form.ModelForm): The form that has a course_id.
        is_required (Boolean): Default True. When True, validates that the
            course_id is not empty.  In all cases, when course_id is supplied,
            validates that it is a valid course.

    Returns:
        (CourseKey) The cleaned and validated course_id as a CourseKey.

    NOTE: Use this method in model forms instead of a custom "clean_course_id" method!

    """
    cleaned_id = model_form.cleaned_data["course_id"]

    if not cleaned_id and not is_required:
        return None

    try:
        course_key = CourseKey.from_string(cleaned_id)
    except InvalidKeyError:
        msg = u'Course id invalid. Entered course id was: "{0}".'.format(cleaned_id)
        raise forms.ValidationError(msg)

    if not modulestore().has_course(course_key):
        msg = u'Course not found. Entered course id was: "{0}".'.format(text_type(course_key))
        raise forms.ValidationError(msg)

    return course_key
