import numpy
import scipy

import Morph.operators


def _unique(image):
    ar = image[image != 0]
    return numpy.unique(ar)


def _minimum(input_, labels, index):
    return scipy.ndimage.minimum(input_, labels, index)


def _nonzero(a):
    return numpy.nonzero(a)


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
