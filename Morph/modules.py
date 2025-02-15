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
