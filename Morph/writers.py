import csv


def xenium(file, image, data):
    with open(file, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=['cell_id', 'group'])
        dict_writer.write_header()
        for g, x, y in zip(data['g'], data['x'], data['y']):
            dict_writer.write({'cell_id': g, 'group': image[x, y]})
