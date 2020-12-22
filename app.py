import sys, os
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from analyzer import get_networks

class App(QWidget):
    
    def __init__(self):
        # Gets current wireless interface and then outputs the currently connected BSSID to a file for later use
        os.system("iw dev | awk '$1==\"Interface\"{print $2}' > /tmp/wireless_interfaces")
        interface = str(open("/tmp/wireless_interfaces", "r").readline()).strip()
        os.system("rm /tmp/wireless_interfaces")
        os.system("iwconfig %s | sed -n 's/.*Access Point: \([0-9\:A-F]\{17\}\).*/\\1/p' > /tmp/current_bssid" %interface)
        
        # Places the wireless card into monitor mode. Internet it unusable while in monitor mode.
        os.system("bash monup.bash")

        super().__init__()
        self.title = 'Wi-Fi Analyzer'
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

        current_bssid = open("/tmp/current_bssid", "r").readline().strip()
        wifi_networks = get_networks()

        # Brings wireless card back into managed mode
        os.system("bash mondown.bash")

        # Values based on wifi_networks list
        numRows = len(wifi_networks)
        numCols = len(wifi_networks[0])

        # Set table size based on wifi_networks list
        self.tableWidget.setColumnCount(numCols)
        self.tableWidget.setRowCount(numRows)

        # Added appropriate headers
        self.tableWidget.setHorizontalHeaderLabels(('BSSID', 'SSID', 'Signal dBm','Channel','Security'))
        self.tableWidget.verticalHeader().setVisible(False)

        # Populate the table
        for row in range(numRows):
            for column in range(numCols):
                self.tableWidget.setItem(row, column, QTableWidgetItem((str(wifi_networks[row][column]))))
                if (str(wifi_networks[row][0]).lower() == str(current_bssid).lower()):
                    self.tableWidget.item(row,column).setBackground(QtGui.QColor('cyan'))
                elif (row%2) == 0:
                    self.tableWidget.item(row,column).setBackground(QtGui.QColor('white'))
                else:
                    self.tableWidget.item(row,column).setBackground(QtGui.QColor('gray'))


        #Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
