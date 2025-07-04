import numpy
import scipy

import Morph.operators

PI = numpy.pi


def _unique(image):
    ar = image[image != 0]
    return numpy.unique(ar)


def _minimum(input_, labels, index):
    return scipy.ndimage.minimum(input_, labels, index)


def _nonzero(a):
    return numpy.nonzero(a)


def _any(a):
    return numpy.any(a)


def _isin(element, test_elements):
    return numpy.isin(element, test_elements)


def _padding_func(vector, iaxis_pad_width, iaxis, kwargs):
    pad = kwargs.get('pad')
    vector[:iaxis_pad_width[0]] = pad[0]
    vector[-iaxis_pad_width[1]:] = pad[-1]
    pad[0] = 1 - pad[0]
    pad[-1] = 1 - pad[-1]


def _distance(image, sampling, border_value, tissue, method):
    if tissue is None:
        tissue = numpy.ones_like(image)
    image[tissue == 0] = border_value
    if method == 'visium':
        shape = 2 * image.shape[0] - image.shape[1], image.shape[1]
        unmapped = numpy.ones(shape, bool)
        grid = numpy.indices(shape)
        checkerboard = 1 - sum(grid) % 2
        x, y = _nonzero(checkerboard)
        unmapped[x, y] = image[(x + y) // 2, y]
        image = unmapped
        sampling = [50, 50 * 3**0.5]
    pad_width = 1
    pad = [0, 1] if method == 'visium' and not border_value else [border_value]
    input_ = numpy.pad(image, pad_width, _padding_func, pad=pad)
    distances = scipy.ndimage.distance_transform_edt(input_, sampling)
    distances = distances[pad_width:-pad_width, pad_width:-pad_width]
    if method == 'visium':
        shape = sum(distances.shape) // 2, distances.shape[1]
        mapped = numpy.zeros(shape)
        mapped[(x + y) // 2, y] = distances[x, y]
        distances = mapped
    distances[tissue == 0] = 0
    return distances


def _layer(image, structure, border_value, tissue):
    if tissue is None:
        tissue = numpy.ones_like(image)
    image[tissue == 0] = border_value
    layers = image * 1
    while _any(image):
        layers += scipy.ndimage.binary_erosion(image,
                                               structure,
                                               output=image,
                                               border_value=border_value)
    layers[tissue == 0] = 0
    return layers


def _count(image):
    x = image[image != 0]
    return numpy.unique_counts(x)


def _maximum(input_, labels, index):
    return scipy.ndimage.maximum(input_, labels, index)


class Center():
    def geodesic(self, image, element=None):
        propagation = Morph.operators.propagation_function(image, element)
        index = _unique(image)
        minimum = _minimum(propagation, image, index)
        centers = {}
        for i, m in zip(index, minimum):
            points = _nonzero((image == i) & (propagation == m))
            centers[i] = set(zip(*points))
        return centers

    def ultimate(self, image, element=None):
        index = _unique(image)
        centers = {i: set() for i in index}
        while _any(image):
            eroded = Morph.operators.erosion(image, element)
            reconstructed = Morph.operators.reconstruction_by_dilation(
                eroded, image, element)
            points = _nonzero(image - reconstructed)
            for point in zip(*points):
                i = image[point]
                centers[i].add(point)
            image = eroded
        return centers


class Distance:
    def minimum(self, image, index=None, tissue=None, d=1, method=None):
        image = image != 0 if index is None else _isin(image, list(index))
        distances = _distance(~image, d, 0, tissue, method)
        distances -= _distance(image, d, 1, tissue, method)
        return distances

    def maximum(self, image, index=None, tissue=None, d=1, method=None):
        image = image != 0 if index is None else _isin(image, list(index))
        distances = _distance(~image, d, 1, tissue, method)
        distances -= _distance(image, d, 0, tissue, method)
        return distances


class Layer():
    def minimum(self, image, index=None, tissue=None, element=None):
        image = image != 0 if index is None else _isin(image, list(index))
        layers = _layer(~image, element, 0, tissue)
        layers -= _layer(image, element, 1, tissue)
        return layers

    def maximum(self, image, index=None, tissue=None, element=None):
        image = image != 0 if index is None else _isin(image, list(index))
        layers = _layer(~image, element, 1, tissue)
        layers -= _layer(image, element, 0, tissue)
        return layers


class Shape():
    def roundness(self, image, element=None):
        propagation = Morph.operators.propagation_function(image, element)
        index, size = _count(image)
        maximum = _maximum(propagation, image, index)
        shape = 4 * size / (PI * maximum**2)
        return dict(zip(index, shape))


class Size():
    def count(self, image):
        index, size = _count(image)
        return dict(zip(index, size))
