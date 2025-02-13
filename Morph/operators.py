import numpy
import skimage


def erosion(image, element=None):
    return skimage.morphology.erosion(image, element)


def dilation(image, element=None):
    return skimage.morphology.dilation(image, element)


def opening(image, element=None):
    return skimage.morphology.opening(image, element)


def closing(image, element=None):
    return skimage.morphology.closing(image, element)


def geodesic_erosion(marker_image, mask_image, element=None):
    image = erosion(marker_image, element)
    return numpy.maximum(mask_image, image)


def geodesic_dilation(marker_image, mask_image, element=None):
    image = dilation(marker_image, element)
    return numpy.minimum(mask_image, image)


def reconstruction_by_erosion(marker_image, mask_image, element=None):
    method = 'erosion'
    image = skimage.morphology.reconstruction(
        marker_image, mask_image, method, element)
    dtype = marker_image.dtype
    return image.astype(dtype)
