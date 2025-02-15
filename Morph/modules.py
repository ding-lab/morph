class Mapper:
    def naive(self, data):
        return data

    def visium(self, data):
        for datum in data:
            datum['x'] = (datum['x'] + datum['y']) // 2
        return data
