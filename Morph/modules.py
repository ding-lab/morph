import numpy


def _floor(x):
    return numpy.astype(x, int)


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
