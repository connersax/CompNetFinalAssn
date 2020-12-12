import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Test'
        self.left = 0
        self.top = 0
        self.width = 1100
        self.height = 400

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show window widget
        self.show()

    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()

        # Make this less hardcoded
        wifi_networks = [
                ["The Pit Of Dispair", "52:6e:de:5c:58:25", 6, -64, "{WPA2/PSK}"],
                ["The Pit Of Despair", "84:a0:6e:f0:7f:46", 11, -49, "{WPA2/PSK}"],
                ["DirtyBirdy", "50:c7:bf:31:60:96", 10, -88, "{WPA/PSK, WPA2/PSK}"],
                ["hello there", "a8:6a:bb:e6:8f:0e", 1, -89, "{WEP}"],
                ["Lalonde", "10:be:f5:26:11:c8", 11, -91, "{WPA/PSK, WPA2/PSK}"],
                ["COGECO-ABB00", "84:0b:7c:8a:bb:08", 11, -88, "{WPA2/PSK}"]]

        # Values based on wifi_networks list
        numRows = len(wifi_networks)
        numCols = len(wifi_networks[0])

        # Set table size based on wifi_networks list
        self.tableWidget.setColumnCount(numCols)
        self.tableWidget.setRowCount(numRows)

        # Added appropriate headers
        self.tableWidget.setHorizontalHeaderLabels(('SSID', 'BSSID', 'Channel','Signal dBm','Security'))
        self.tableWidget.verticalHeader().setVisible(False)

        # Populate the table
        for row in range(numRows):
            for column in range(numCols):
                # Set numbers to strings?
                # if isinstance(wifi_networks[row][column],type(num)):
                #
                # else:
                self.tableWidget.setItem(row, column, QTableWidgetItem((wifi_networks[row][column])))


        #Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
