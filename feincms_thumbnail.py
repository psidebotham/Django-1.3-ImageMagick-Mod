import os

from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from paver.easy import sh
import re

register = template.Library()


def tryint(v):
    try:
        return int(v)
    except ValueError:
        return 999999 # Arbitrarily big number


@register.filter
def thumbnail(filename, size='200x200'):
    """
    Creates a thumbnail from the image passed, returning its path::

        {{ object.image.name|thumbnail:"400x300" }}

    You have to pass the ``name``, not the ``url`` attribute of an ``ImageField``
    or ``FileField``. The thumbnail filter only works for images inside
    ``MEDIA_ROOT``.

    The dimensions passed are treated as a bounding box. The aspect ratio of
    the initial image is preserved. Images aren't blown up in size if they
    are already smaller.

    Both width and height must be specified. If you do not care about one
    of them, just set it to an arbitrarily large number::

        {{ object.image.name|thumbnail:"300x999999" }}
    """

    if not (filename and 'x' in size):
        # Better return empty than crash
        return u''

    # defining the size
    x, y = [tryint(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    try:
        basename, format = filename.rsplit('.', 1)
    except ValueError:
        basename, format = filename, 'jpg'
    miniature = basename + '_thumb_' + size + '.' +  format
    miniature_filename = os.path.join(settings.MEDIA_ROOT, miniature).encode('utf-8')
    miniature_url = os.path.join(settings.MEDIA_URL, miniature).encode('utf-8')
    orig_filename = os.path.join(settings.MEDIA_ROOT, filename).encode('utf-8')
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename) or (os.path.getmtime(miniature_filename)<os.path.getmtime(orig_filename)):
        #try:
        cmd = 'convert "{basename}" -resize {x}x{y}\> "{newname}"'.format(
            basename=orig_filename, 
            x=x, 
            y=y, 
            newname=miniature_filename)
        sh(cmd)
        #except:
        #    return os.path.join(settings.MEDIA_URL, filename)
    return force_unicode(miniature_url)


@register.filter
def cropscale(filename, size='200x200'):
    """
    Scales the image down and crops it so that its size equals exactly the size
    passed (as long as the initial image is bigger than the specification).
    """

    if not (filename and 'x' in size):
        # Better return empty than crash
        return u''

    w, h = [tryint(x) for x in size.split('x')]

    try:
        basename, format = filename.rsplit('.', 1)
    except ValueError:
        basename, format = filename, 'jpg'
    miniature = basename + '_cropscale_' + size + '.' +  format
    miniature_filename = os.path.join(settings.MEDIA_ROOT, miniature).encode('utf-8')
    miniature_url = os.path.join(settings.MEDIA_URL, miniature).encode('utf-8')
    orig_filename = os.path.join(settings.MEDIA_ROOT, filename).encode('utf-8')
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename) or (os.path.getmtime(miniature_filename)<os.path.getmtime(orig_filename)):
        #try:
        cmd = 'convert "{basename}" -resize {x}x{y}^ -gravity center -extent {x}x{y} "{newname}"'.format(
            basename=orig_filename, 
            x=x, 
            y=y, 
            newname=miniature_filename)
        sh(cmd)
        #except:
        #    return os.path.join(settings.MEDIA_URL, filename)
        
    return force_unicode(miniature_url)
