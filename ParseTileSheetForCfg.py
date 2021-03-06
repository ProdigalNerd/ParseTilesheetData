import json
import os

sorted_tiles = {}

with open("EternalFacadeTiles.json") as tile_data:
    tiles = json.load(tile_data)

    for tile in tiles['frames']:
        fname_segments = tile['filename'].split('/')
        numSegments = len(fname_segments)

        if not fname_segments[numSegments - 2] in sorted_tiles:
            sorted_tiles[fname_segments[numSegments - 2]] = []

        sorted_tiles[fname_segments[numSegments - 2]].append(tile)

    for key, values in sorted_tiles.items():
        first_item = values[0] # first item in the array of tiles for that folder
        tmp_segments = first_item['filename'].split('/') # folder segments
        num_tmpSegments = len(tmp_segments) # number of nested folders
        n_file_path = "tiles/"

        for x in range(0, num_tmpSegments - 2):
            n_file_path += tmp_segments[x] + "/"

        if n_file_path != '':
            if not os.path.exists(n_file_path):
                os.makedirs(n_file_path)

        for i in range(0, len(values)):
            fname_segments = values[i]['filename'].split('/')
            numSegments = len(fname_segments)

            fname_parts = fname_segments[numSegments - 1].replace('-', '_').replace('.png', '').split('_')

            base_file_name = ""
            for k in range(0, len(fname_parts)):
                if fname_parts[k].isnumeric():
                    for j in range(0, k):
                        base_file_name += fname_parts[j].upper()

                        if j < (k - 1):
                            base_file_name += "_"

            if base_file_name == '':
                base_file_name = fname_segments[numSegments - 1].split('.')[0].replace('-', '_').upper() + ".cfg"
            else:
                base_file_name += ".cfg"

            #file_name = fname_segments[numSegments - 1].split('.')[0].replace('-', '_').upper() + ".cfg"

            with open(os.path.join(n_file_path, base_file_name), 'a') as py_file:
                if os.path.getsize(os.path.join(n_file_path, base_file_name)) > 0:
                    py_file.write(',\n')

                py_file.write("//\n")
                py_file.write("// This has been auto-generated by ParseTileSheetForCfg Python App \n")
                py_file.write("// Config for " + fname_segments[numSegments - 1] + " \n")
                py_file.write("// Author Tyler Wilson <bearmetal09@gmail.com>\n")
                py_file.write("//\n")

                tile_x = int(sorted_tiles[key][i]["frame"]["x"])
                tile_y = int(sorted_tiles[key][i]["frame"]["y"])

                py_file.write('{\n')
                py_file.write('\tx = ' + str(tile_x) + ';\n')
                py_file.write('\ty = ' + str(tile_y) + ';\n')
                py_file.write('}')


