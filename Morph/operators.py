import skimage


def erosion(image, element=None):
    return skimage.morphology.erosion(image, element)


def dilation(image, element=None):
    return skimage.morphology.dilation(image, element)


def opening(image, element=None):
    return skimage.morphology.opening(image, element)


def closing(image, element=None):
    return skimage.morphology.closing(image, element)
