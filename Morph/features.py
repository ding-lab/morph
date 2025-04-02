import numpy
import scipy

import Morph.operators


def _propagation(image, element):
    objects = scipy.ndimage.find_objects(image)
    propagation = numpy.zeros_like(image)
    for i in range(len(objects)):
        if objects[i]:
            region = image[objects[i]] + 0
            region[image[objects[i]] != i + 1] = 0
            propagation[objects[i]] += Morph.operators.propagation_function(region, element)
    return propagation


def _unique(image):
    ar = image[image != 0]
    return numpy.unique(ar)


def _minimum(input_, labels, index):
    return scipy.ndimage.minimum(input_, labels, index)


def _where(condition):
    return numpy.where(condition)


def _any(a):
    return numpy.any(a)


def _count(image):
    x = image[image != 0]
    return numpy.unique_counts(x)


def _maximum(input_, labels, index):
    return scipy.ndimage.maximum(input_, labels, index)


class Center:
    def geodesic(self, image, element=None):
        propagation = _propagation(image, element)
        index = _unique(image)
        minimum = _minimum(propagation, image, index)
        centers = {}
        for i, m in zip(index, minimum):
            points = _where((image == i) & (propagation == m))
            centers[i] = set(zip(*points))
        return centers

    def ultimate(self, image, element=None):
        index = _unique(image)
        centers = {i: set() for i in index}
        while _any(image):
            eroded = Morph.operators.erosion(image, element)
            reconstructed = Morph.operators.reconstruction_by_dilation(eroded, image, element)
            points = _where(image - reconstructed)
            for point in zip(*points):
                i = image[point]
                centers[i].add(point)
            image = eroded
        return centers


class Shape:
    def roundness(self, image, element=None):
        propagation = _propagation(image, element)
        index, size = _count(image)
        maximum = _maximum(propagation, image, index)
        shape = 4 * size / (numpy.pi * maximum ** 2)
        return dict(zip(index, shape))


class Size:
    def count(self, image):
        index, size = _count(image)
        return dict(zip(index, size))


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
