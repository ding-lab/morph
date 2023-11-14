import numpy
import skimage


def erosion(image, element=None):
    return skimage.morphology.erosion(image, element)


def dilation(image, element=None):
    return skimage.morphology.dilation(image, element)


def layering(image, element=None):
    eroded = erosion(image, element)
    layers = image - eroded
    while numpy.max(eroded):
        image = eroded
        eroded = erosion(image, element)
        layers = layers + (image - eroded) * (numpy.max(layers) + 1)
    return layers
