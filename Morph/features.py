import numpy
import scipy

import Morph.operators


def geodesic_center(image):
    image = Morph.operators.propagation_function(image)
    return set([(x, y) for x, y in zip(*numpy.where(image == image[image > 0].min()))])


def ultimate_center(image, element=None):
    points = []
    while len(image[image > 0]):
        eroded = Morph.operators.erosion(image, element)
        c = image - Morph.operators.reconstruction_by_dilation(eroded, image, element)
        points += [(x, y) for x, y in zip(*numpy.where(c > 0))]
        image = eroded
    return set(points)


def layering(image, element=None, method='guaranteed', tissue=1):
    if method == 'guaranteed':
        minimum = layering(image, element, method='minimum')
        indexes = minimum == layering(image, element, 'maximum', tissue)
        layers = numpy.full(image.shape, None)
        layers[indexes] = minimum[indexes]
        return layers
    mask = tissue if method == 'minimum' else Morph.operators.erosion(tissue, element)
    eroded = Morph.operators.erosion(image, element)
    layers = numpy.multiply(image - eroded, mask)
    while not (image == eroded + tissue - mask).all():
        image = eroded + tissue - mask
        eroded = Morph.operators.erosion(image, element)
        layers = layers + \
            numpy.multiply(image - eroded, mask) * (numpy.max(layers) + 1)
    return layers


def distance(image):
    return scipy.ndimage.distance_transform_edt(image)


def count(image):
    return len(image[image > 0])


def roundness(image, element=None):
    return 4 * count(image) / (3.14 * Morph.operators.propagation_function(image, element).max().astype(int) ** 2)
