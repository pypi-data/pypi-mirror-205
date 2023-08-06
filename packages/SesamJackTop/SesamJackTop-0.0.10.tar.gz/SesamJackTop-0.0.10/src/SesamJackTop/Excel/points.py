"""     This module is to read excel imports to python     """

import openpyxl

class Node:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

def load_nodes(filename, sheetname):
    workbook = openpyxl.load_workbook(filename)
    worksheet = workbook[sheetname]

    nodes = []
    for row in worksheet.iter_rows(min_row=2, max_col=4, values_only=True):
        node = Node(*row)
        nodes.append(node)

    return nodes