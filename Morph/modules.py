import numpy


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
