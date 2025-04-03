import multiprocessing
import numpy
import scipy
import skimage


def _propagation_function(image, x, y, element=None):
    dilated = numpy.zeros_like(image)
    dilated[x, y] = 1
    reconstructed = reconstruction_by_dilation(dilated, image, element)
    i = 0
    while not numpy.array_equal(dilated, reconstructed):
        dilated = geodesic_dilation(dilated, image, element)
        i += 1
    return i


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
    return numpy.astype(image, dtype)


def reconstruction_by_dilation(marker_image, mask_image, element=None):
    method = 'dilation'
    image = skimage.morphology.reconstruction(
        marker_image, mask_image, method, element)
    dtype = marker_image.dtype
    return numpy.astype(image, dtype)


def propagation_function(image, element=None):
    points = numpy.where(image)
    propagation = numpy.zeros_like(image)
    iterable = [(image, x, y, element) for x, y in zip(*points)]
    with multiprocessing.Pool() as pool:
        results = pool.starmap(_propagation_function, iterable)
    for x, y, r in zip(*points, results):
        propagation[x, y] = r
    return propagation


def labeling(image, element=None):
    image, _ = scipy.ndimage.label(image, element)
    return image
