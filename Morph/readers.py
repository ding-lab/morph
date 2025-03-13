import csv
import gzip
import numpy


def xenium(file):
    g = []
    x = []
    y = []
    with gzip.open(file, 'rt') as f:
        dict_reader = csv.DictReader(f)
        for row in dict_reader:
            g.append(row['feature_name'])
            x.append(float(row['x_location']))
            y.append(float(row['y_location']))
    return {'g': g, 'x': numpy.array(x), 'y': numpy.array(y)}
