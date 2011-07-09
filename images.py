"""
Utility functions for handling images.

Requires PIL, as you might imagine.
"""

from django.core.files import File

class ImageFile(File):
    """
    A mixin for use alongside django.core.files.base.File, which provides
    additional features for dealing with images.
    """
    def _get_width(self):
        return self._get_image_dimensions()[0]
    width = property(_get_width)

    def _get_height(self):
        return self._get_image_dimensions()[1]
    height = property(_get_height)

    def _get_image_dimensions(self):
        if not hasattr(self, '_dimensions_cache'):
            close = self.closed
            self.open()
            self._dimensions_cache = get_image_dimensions(self, close=close)
        return self._dimensions_cache

def get_image_dimensions(file_or_path, close=False):
    """
    Returns the (width, height) of an image, given an open file or a path.  Set
    'close' to True to close the file at the end if it is initially in an open
    state.
    """
    from paver.easy import sh, BuildFailure
    import re
    #try:
    output = sh('identify "{0}"'.format(file_or_path), capture=True)
    w, h = re.search(" (\d*)x(\d*) ", output).groups()
    return (int(w), int(h))
    #except BuildFailure:
    
