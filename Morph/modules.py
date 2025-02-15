import numpy
import skimage

import Morph.operators


class Mapper:
    def naive(self, data):
        return data

    def visium(self, data):
        for datum in data:
            datum['x'] = (datum['x'] + datum['y']) // 2
        return data

    def xenium(self, data, d):
        for datum in data:
            datum['x'] = int(datum['x'] / d)
            datum['y'] = int(datum['y'] / d)
        return data

    def custom(self, data, mapper, *args):
        return mapper(data, *args)


class Counter:
    def naive(self, data, G):
        image = {}
        x = max(datum['x'] for datum in data) + 1
        y = max(datum['y'] for datum in data) + 1
        shape = (x, y)
        for datum in data:
            g = datum['g']
            if g in G and g not in image:
                image[g] = numpy.zeros(shape)
                x = datum['x']
                y = datum['y']
                image[g][x, y] = 1
        return image

    def total(self, data, G):
        image = {}
        x = max(datum['x'] for datum in data) + 1
        y = max(datum['y'] for datum in data) + 1
        shape = (x, y)
        for g in G:
            image[g] = numpy.zeros(shape)
        for datum in data:
            g = datum['g']
            x = datum['x']
            y = datum['y']
            image[g][x, y] += 1
        return image

    def custom(self, data, counter, *args):
        return counter(data, *args)


class Muxer:
    def naive(self, image):
        for i in image:
            return image[i]

    def maximum(self, image):
        array = [image[i] for i in image]
        return numpy.maximum.reduce(array)

    def custom(self, data, muxer, *args):
        return muxer(data, *args)


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

    def custom(self, data, morphological_filter, *args):
        return morphological_filter(data, *args)


class Thresholder:
    def naive(self, image):
        return image

    def binary(self, image, tau):
        dtype = image.dtype
        image = image >= tau
        return image.astype(dtype)

    def custom(self, data, thresholder, *args):
        return thresholder(data, *args)


class AlgebraicFilter:
    def naive(self, image):
        return image

    def area_opening(self, image, la):
        dtype = image.dtype
        image = skimage.morphology.remove_small_objects(image, la)
        return image.astype(dtype)

    def area_closing(self, image, la):
        dtype = image.dtype
        image = skimage.morphology.remove_small_holes(image, la)
        return image.astype(dtype)

    def custom(self, data, algebraic_filter, *args):
        return algebraic_filter(data, *args)


class Labeler:
    def naive(self, image):
        return image

    def blob(self, image, element):
        return Morph.operators.labeling(image, element)

    def custom(self, image, labeler, *args):
        return labeler(data, *args)
