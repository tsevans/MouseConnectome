mouse_region_dict = {}
mouse_adj_matrix = []
matrix_info = []


class RegionItem(object):
    def __init__(self, side, module, abbr):
        self.side = side
        self.module = module
        self.abbr = abbr

    def name(self):
        side_str = 'one' if self.side is 1 else 'two'
        return side_str + '_' + self.abbr


def make_weighted_mouse_connectome():
    def read_mouse_weights():
        """
        Reads weights from adjacency matrix.
        :return: Two dimensional array of weights for mouse connectome.
        """
        global mouse_adj_matrix
        if len(mouse_adj_matrix) != 0:
            print('returning pre-made matrix')
            return mouse_adj_matrix
        adj_file = open('data/Mouse_Matrix_Binned.csv', 'r')
        values = []
        skip = 3
        for line in adj_file.readlines():  # Read through each line of csv
            # Skip non-value lines in file
            if skip > 0:
                skip -= 1
                continue
            row = []
            for y in line.split(',')[5:]:  # Read each value in current line
                clean = y.strip('\n')
                if clean.isdigit():
                    row.append(int(clean))
            values.append(row)
        mouse_adj_matrix = values
        adj_file.close()
        return mouse_adj_matrix

    def build_matrix_guidelines():
        """
        Build a list of RegionItems for all entries in the matrix.
        :return: List of RegionItems which describe each area of the connectome matrix.
        """
        adj_file = open('data/Mouse_Matrix_Binned.csv', 'r')
        global matrix_info
        if len(matrix_info) != 0:
            print('returning pre-made guidelines')
            return matrix_info
        lines = adj_file.readlines()
        raw_regions = lines[0].split(',')[5:159]
        raw_abbrs = lines[2].split(',')[5:159]
        info = []
        for x in range(154):
            s = raw_regions[x].strip()
            a = raw_abbrs[x].strip()
            if 0 <= x < 21 or 77 <= x < 98:
                m = 1
            elif 21 <= x < 62 or 98 <= x < 139:
                m = 2
            else:
                m = 3
            r = RegionItem(int(s), m, a)
            info.append(r)
        matrix_info = info
        adj_file.close()
        return matrix_info

    finaldata = open('data/final_mouse_weighted.txt', 'w')
    adj = read_mouse_weights()
    guide = build_matrix_guidelines()
    from_index = 0
    for x in adj:
        to_index = 0
        for y in x:
            fr = guide[from_index]
            to = guide[to_index]
            if y is not 0:
                formatted = '%-13s %-13s %d\n' % (fr.name(), to.name(), y)
                finaldata.write(formatted)
            to_index += 1
        from_index += 1
    finaldata.close()


def get_mouse_region_names():
    """
    Creates mapping of region abbreviations to formal names of regions in mouse brain.
    :return: Dictionary with keys as abbreviations and values as full names.
    """
    dfile = open('data/mouse_regions.txt', 'r')
    global mouse_region_dict
    if len(mouse_region_dict) != 0:
        print('returning pre-made dictionary')
        return mouse_region_dict
    new_dict = {}
    for line in dfile.readlines():
        parts = line.split('\t')
        new_dict[parts[0]] = parts[1].replace('"', '').strip('\n')
    mouse_region_dict = new_dict
    dfile.close()
    return mouse_region_dict


if __name__ == '__main__':
    make_weighted_mouse_connectome()
