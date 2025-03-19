import sys
import psutil
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, \
    QTableWidgetItem, QMainWindow, QAction, QFileDialog
from PyQt5.QtCore import QTimer
class SystemResourceMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Resource Monitor")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.resource_table = QTableWidget()
        self.resource_table.setColumnCount(4)
        self.resource_table.setHorizontalHeaderLabels(["Time", "CPU Usage (%)", "Memory Usage (%)", "Disk Usage (%)"])
        self.layout.addWidget(self.resource_table)
        # Matplotlib setup
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.update_button = QPushButton("Start Monitoring")
        self.layout.addWidget(self.update_button)
        self.update_button.clicked.connect(self.toggle_monitoring)
        self.monitoring = False
        self.save_button = QPushButton("Save to CSV")
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_to_csv)
        self.central_widget.setLayout(self.layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_resource_info)
        self.data = {'time': [], 'cpu': [], 'memory': [], 'disk': []}
        self.init_menu()
    def init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        save_action = QAction('Save to CSV', self)
        save_action.triggered.connect(self.save_to_csv)
        file_menu.addAction(save_action)
    def toggle_monitoring(self):
        if self.monitoring:
            self.update_button.setText("Start Monitoring")
            self.timer.stop()
            self.monitoring = False
        else:
            self.update_button.setText("Stop Monitoring")
            self.timer.start(1000)
            self.monitoring = True
    def update_resource_info(self):
        cpu_percent = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        self.data['time'].append(len(self.data['time']) + 1)
        self.data['cpu'].append(cpu_percent)
        self.data['memory'].append(mem.percent)
        self.data['disk'].append(disk.percent)
        self.resource_table.setRowCount(len(self.data['time']))
        for i in range(len(self.data['time'])):
            row = [self.data['time'][i], self.data['cpu'][i], self.data['memory'][i], self.data['disk'][i]]
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.resource_table.setItem(i, j, item)
        # Update the plot
        self.ax.clear()
        self.ax.plot(self.data['time'], self.data['cpu'], label='CPU Usage (%)')
        self.ax.plot(self.data['time'], self.data['memory'], label='Memory Usage (%)')
        self.ax.plot(self.data['time'], self.data['disk'], label='Disk Usage (%)')
        self.ax.legend()
        self.canvas.draw()
    def save_to_csv(self):
        if self.data['time']:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
            if file_path:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Time", "CPU Usage (%)", "Memory Usage (%)", "Disk Usage (%)"])
                    writer.writerows(zip(self.data['time'], self.data['cpu'], self.data['memory'], self.data['disk']))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemResourceMonitor()
    window.show()
    sys.exit(app.exec_())
