'''
Created on 18.07.2021

@author: kai
'''
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class TableModel_(QtCore.QAbstractTableModel):
    
    #header_labels = ['Amount', 'Unit', 'Ingredient']
    
    def __init__(self, data, header_labels):
        super(TableModel_, self).__init__()
        self._data = data
        self.header_labels = header_labels

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)