import csv
import gzip
import numpy


def transcripts(file):
    g = []
    v = []
    x = []
    y = []
    with gzip.open(file, 'rt') as f:
        dict_reader = csv.DictReader(f)
        for row in dict_reader:
            g.append(row['feature_name'])
            v.append(1)
            x.append(float(row['x_location']))
            y.append(float(row['y_location']))
    return {'g': g, 'v': v, 'x': numpy.array(x), 'y': numpy.array(y)}


def cells(file):
    g = []
    v = []
    x = []
    y = []
    with gzip.open(file, 'rt') as f:
        dict_reader = csv.DictReader(f)
        for row in dict_reader:
            g.append(row['cell_id'])
            v.append(1)
            x.append(float(row['x_centroid']))
            y.append(float(row['y_centroid']))
    return {'g': g, 'v': v, 'x': numpy.array(x), 'y': numpy.array(y)}
