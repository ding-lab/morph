import numpy

import Morph.operators


def _floor(x):
    return numpy.astype(x, int)


def _count(data, G, method):
    G = G & set(data['g'])
    image = {}
    X = max(data['x'])
    Y = max(data['y'])
    shape = (X + 1, Y + 1)
    for g in G:
        image[g] = numpy.zeros(shape, int)
    for g, v, x, y in zip(data['g'], data['v'], data['x'], data['y']):
        if g in G:
            image[g][x, y] += v
            if method == 'naive':
                G.remove(g)
    return image


def _point_wise_maximum(image):
    array = [image[i] for i in image]
    return numpy.maximum.reduce(array)


class Mapper:
    def naive(self, data):
        return data

    def visium(self, data):
        x = (data['x'] + data['y']) // 2
        return {'g': data['g'], 'v': data['v'], 'x': x, 'y': data['y']}

    def xenium(self, data, d):
        x = _floor(data['x'] / d)
        y = _floor(data['y'] / d)
        return {'g': data['g'], 'v': data['v'], 'x': x, 'y': y}

    def custom(self, data, mapper, *args):
        return mapper(data, *args)


class Counter:
    def naive(self, data, G):
        return _count(data, G, Counter.naive.__name__)

    def total(self, data, G):
        return _count(data, G, Counter.total.__name__)

    def custom(self, data, counter, *args):
        return counter(data, *args)


class Muxer:
    def naive(self, image):
        _, image = image.popitem()
        return image

    def maximum(self, image):
        return _point_wise_maximum(image)

    def custom(self, image, muxer, *args):
        return muxer(image, *args)


class MorphologicalFilter:
    def naive(self, image):
        return image

    def opening(self, image, element):
        return Morph.operators.opening(image, element)

    def closing(self, image, element):
        return Morph.operators.closing(image, element)

    def open_close(self, image, element):
        image = Morph.operators.opening(image, element)
        return Morph.operators.closing(image, element)

    def close_open(self, image, element):
        image = Morph.operators.closing(image, element)
        return Morph.operators.opening(image, element)

    def custom(self, image, morphological_filter, *args):
        return morphological_filter(image, *args)


class Thresholder:
    def naive(self, image):
        return image

    def binary(self, image, tau):
        return image >= tau
