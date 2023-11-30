import numpy
import skimage


def erosion(image, element=None):
    return skimage.morphology.erosion(image, element)


def dilation(image, element=None):
    return skimage.morphology.dilation(image, element)


def layering(image, element=None, method='guaranteed', tissue=1):
    if method == 'guaranteed':
        minimum = layering(image, element, method='minimum')
        indexes = minimum == layering(image, element, 'maximum', tissue)
        layers = numpy.full(image.shape, None)
        layers[indexes] = minimum[indexes]
        return layers
    mask = tissue if method == 'minimum' else erosion(tissue, element)
    eroded = erosion(image, element)
    layers = numpy.multiply(image - eroded, mask)
    while not (image == eroded + tissue - mask).all():
        image = eroded + tissue - mask
        eroded = erosion(image, element)
        layers = layers + \
            numpy.multiply(image - eroded, mask) * (numpy.max(layers) + 1)
    return layers
