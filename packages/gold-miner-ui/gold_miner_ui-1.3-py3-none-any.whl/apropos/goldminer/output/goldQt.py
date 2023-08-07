import sys
import json
import multiprocessing
import threading
import time
import queue
from apropos.goldminer.output.goldOutput import GoldOutput

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateTimeEdit,
    QDial,
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollBar,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QStyleFactory,
    QTableWidget,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg


class QtDataViewer(QDialog):
    def __init__(self, q, parent=None):
        super(QtDataViewer, self).__init__(parent)

        self.queue = q

        vertLayout = QVBoxLayout()

        # create a graph
        self.graph = PlotWidget()
        vertLayout.addWidget(self.graph)

        # set styles
        self.graph.setBackground("w")
        self.graph.setTitle("gold-miner analysis")
        self.pen = pg.mkPen(color=(0, 0, 255))

        # a container for storing data by identifier
        self.data = {}

        # create a label strip # TODO: make a table
        horizLayout = QHBoxLayout()
        vertLayout.addLayout(horizLayout)
        # mainLayout.addLayout(horizLayout)

        # set up labels
        self.textLabel = QLabel("identifier:")
        horizLayout.addWidget(self.textLabel)

        self.identifier_value = QLabel("no data")
        horizLayout.addWidget(self.identifier_value)

        self.confidence_label = QLabel("confidence:")
        horizLayout.addWidget(self.confidence_label)

        self.confidence_value = QLabel("no data")
        horizLayout.addWidget(self.confidence_value)

        # set timer to ask for redisplay every so often
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_update)
        self.timer.start(100)

        # connect the final layout
        self.setLayout(vertLayout)

    def timer_update(self):
        item = None
        # print(f"here: {self.queue} {self.queue.qsize()}")
        while not self.queue.empty():
            item = self.queue.get()[0]
            (tstamp, identifier, label, confidence, count) = item
            if identifier not in self.data:
                self.data[identifier] = {
                    "time": [tstamp],
                    "confidence": [confidence],
                    "label": label,
                }
                self.data[identifier]["line"] = self.graph.plot(
                    self.data[identifier]["time"],
                    self.data[identifier]["confidence"],
                    pen=self.pen,
                    name=identifier,
                )
                self.graph.addLegend()
            else:
                self.data[identifier]["time"].append(tstamp)
                self.data[identifier]["confidence"].append(confidence)
                self.data[identifier]["line"].setData(
                    self.data[identifier]["time"], self.data[identifier]["confidence"]
                )

        for identifier in self.data:
            self.data[identifier]["line"].setData(
                self.data[identifier]["time"], self.data[identifier]["confidence"]
            )
        # if not self.didone:
        #     hour = [1,2,3,4,5,6,7,8,9,10,11,12]
        #     temperature = [30,32,34,32,33,31,29,32,35,45,-5,10]
        #     self.graph.plot(hour, temperature)
        #     self.didone = True


class GoldQt(GoldOutput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queue = multiprocessing.Queue()
        t = multiprocessing.Process(target=self.start_viewer, args=[self.queue])
        # t = threading.Thread(target=self.start_viewer, args=[self.queue])
        t.daemon = True
        t.start()

    def start_viewer(self, q):
        self.app = QApplication(sys.argv)
        self.viewer = QtDataViewer(q)
        self.viewer.show()
        self.app.exec()
        print("viewer quit")

    def output(self, analysis_results, packet_number, tunnel_count, subscriptions):
        # print(f"here: {analysis_results}")
        self.queue.put(analysis_results)
        time.sleep(0.1)

    def close(self):
        pass
        # TODO: stop the app
