import csv


def xenium(file, image, data):
    with open(file, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=['cell_id', 'group'])
        dict_writer.writeheader()
        for g, x, y in zip(data['g'], data['x'], data['y']):
            dict_writer.writerow({'cell_id': g, 'group': image[x, y]})


def xenium_dict(file, feature):
    with open(file, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=['group', 'feature'])
        dict_writer.writeheader()
        for f in feature:
            dict_writer.writerow({'group': f, 'feature': feature[f]})
