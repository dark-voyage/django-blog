from django.core.cache import cache
from django.db.models import ManyToManyField
from django.utils import timezone
from django.utils.text import slugify
import xml.etree.ElementTree


def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """

    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug


# UPDATING INSTANCE'S MODEL VALUES WITH GIVEN DICT
def update_object_values(obj, dict):  # requires object and dictionary. Set values to the object
    manytomany_fields = ['department']
    image_list = ['image', 'icon', 'photo', 'background_image']
    for attr, value in dict.items():

        if hasattr(obj, attr):
            if attr in image_list and attr is None:
                pass
            else:
                setattr(obj, attr, value)
    obj.save()


# GENERATING UNIQUE ID
# def unique_number_generator(klass, length, attribute='order_number'):
def unique_number_generator(klass, length, instance, type):
    last_id = klass.objects.filter(order_number__startswith=type).exclude(id=instance.id).order_by('id').last()

    if not last_id or not last_id.order_number:  # return initial number
        initial = (length - 1) * "0" + '1'
        return initial

    number = last_id.order_number
    number = number.replace(type, '')

    number = int(number) + 1
    formatted = (length - len(str(number))) * "0" + str(number)
    return str(formatted)


# Simple boolean checke for HTML checker
def boolen_checker(value):
    if value == "on":
        return True
    return False


# Auto generate model
def generate_field(field):
    try:
        result = translate.translate_to_latin(field)
        return result
    except Exception:
        pass


# GET AUTO HITCOUNT INCREMENT
def auto_increment(request, instance):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    content_type = instance.__class__.__name__.lower()

    key = f"{content_type}-{ip}-{instance.id}"

    current_data = cache.get(key)
    if not current_data:
        new_data = cache.set(key, timezone.now().time(), 600)
        attributes = ['views', 'hit']
        for item in attributes:
            if hasattr(instance, item):
                get = getattr(instance, item)
                get += 1
                setattr(instance, item, get)
                instance.save()
                break


def remove_tags(raw_html):
    import re
    CLEANR = re.compile('<.*?>')
    cleantext = re.sub(CLEANR, '', raw_html)
    return "".join(cleantext.split())
