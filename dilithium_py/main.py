import matplotlib
matplotlib.use('Qt5Agg')
import os
from PyQt5 import QtWidgets, QtGui, QtCore
import sys 
from dilithium import Dilithium2, Dilithium3, Dilithium5
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time 
import psutil

 
def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024
    
def get_cpu_usage():
    return psutil.cpu_percent(interval=None)

def estimate_power_consumption(cpu_usage, duration, base_power=15):
    return (cpu_usage / 100) * base_power * duration

class MyApp(QtWidgets.QMainWindow): 
    def init(self, parent=None):
        super().init(parent) 
        self.setupUi(self) 
 
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 960)
        MainWindow.setStyleSheet("QWidget {\n"
"    background-color: #2e2e2e;  /* Slightly dark gray */\n"
"    color: #ffffff;  /* Default text color */\n"
"    font: 12px \"Arial\";  /* Default font */\n"
"}")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(20, 20, 1190, 91)
        self.textEdit.setPlaceholderText("Type Here ...")
        self.textEdit.setStyleSheet("QTextEdit {\n"
"    background-color: #d6d6d6;  /* Slightly white background */\n"
"    color: #333333;  /* Dark gray text for contrast */\n"
"    border: 2px solid #cccccc;  /* Light gray border */\n"
"    border-radius: 8px;  /* Rounded corners */\n"
"    padding: 8px;  /* Internal padding for text */\n"
"    font: 12px \"Arial\";  /* Font style */\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"QTextEdit:hover {\n"
"    border: 2px solid #bbbbbb;  /* Slightly darker border on hover */\n"
"}\n"
"\n"
"QTextEdit:focus {\n"
"    border: 2px solid #aaaaaa;  /* Highlighted border on focus */\n"
"    background-color: #ffffff;  /* Brighter background on focus */\n"
"}")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(1220, 20, 125, 35))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("dilithium2")
        self.comboBox.addItem("dilithium3")
        self.comboBox.addItem("dilithium5")
        self.comboBox.setStyleSheet("QComboBox {\n"
"    background-color: #a9e1ff;  /* Slightly white background */\n"
"    color: #333333;  /* Dark gray text for contrast */\n"
"    border: 2px solid #cccccc;  /* Light gray border */\n"
"    border-radius: 8px;  /* Rounded corners */\n"
"    padding: 8px 16px;  /* Button padding */\n"
"    font: bold 12px \"Arial\";  /* Font style */\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #eaeaea;  /* Slightly darker background on hover */\n"
"    border: 2px solid #bbbbbb;  /* Slightly darker border on hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #dddddd;  /* Even darker background on press */\n"
"    border: 2px solid #aaaaaa;  /* Darker border on press */\n"
"}")
        self.selected_enc = "dilithium2"
        self.comboBox.currentIndexChanged.connect(self.handle_enc)
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox.setItemText(0, _translate("MainWindow", "dilithium2"))
        self.comboBox.setItemText(1, _translate("MainWindow", "dilithium3"))
        self.comboBox.setItemText(2, _translate("MainWindow", "dilithium5"))
        

        self.pushButton = QtWidgets.QPushButton("Sign and Verify", self.centralwidget)
        self.pushButton.setGeometry(20, 130, 211, 51)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton {\n"
"    background-color: #a9e1ff;  /* Slightly white background */\n"
"    color: #333333;  /* Dark gray text for contrast */\n"
"    border: 2px solid #cccccc;  /* Light gray border */\n"
"    border-radius: 8px;  /* Rounded corners */\n"
"    padding: 8px 16px;  /* Button padding */\n"
"    font: bold 12px \"Arial\";  /* Font style */\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #eaeaea;  /* Slightly darker background on hover */\n"
"    border: 2px solid #bbbbbb;  /* Slightly darker border on hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #dddddd;  /* Even darker background on press */\n"
"    border: 2px solid #aaaaaa;  /* Darker border on press */\n"
"}")

        self.encryptiontable = QtWidgets.QTableView(self.centralwidget)
        self.encryptiontable.setGeometry(20, 360, 391, 321)
        self.encryptiontable.setStyleSheet("QTableView {\n"
"    background-color: #f7f7f7;  /* Slightly white background */\n"
"    color: #333333;  /* Dark gray text for contrast */\n"
"    border: 2px solid #cccccc;  /* Light gray border */\n"
"    border-radius: 8px;  /* Rounded corners */\n"
"    gridline-color: #dddddd;  /* Light gray grid lines */\n"
"    font: 12px \"Arial\";  /* Font style */\n"
"    selection-background-color: #eaeaea;  /* Light gray selection background */\n"
"    selection-color: #000000;  /* Black text for selected items */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #eeeeee;  /* Light gray header background */\n"
"    color: #333333;  /* Dark gray header text */\n"
"    border: 1px solid #cccccc;  /* Light gray border for headers */\n"
"    padding: 4px;  /* Padding for header text */\n"
"    font: bold 12px \"Arial\";  /* Font style for headers */\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"    background-color: #eeeeee;  /* Light gray corner button */\n"
"    border: 1px solid #cccccc;  /* Border for corner button */\n"
"}")

        self.viewtable = QtWidgets.QTableView(self.centralwidget)
        self.viewtable.setGeometry(20, 200, 391, 141)
        self.viewtable.setStyleSheet("QTableView {\n"
"    background-color: #f7f7f7;  /* Slightly white background */\n"
"    color: #333333;  /* Dark gray text for contrast */\n"
"    border: 2px solid #cccccc;  /* Light gray border */\n"
"    border-radius: 8px;  /* Rounded corners */\n"
"    gridline-color: #dddddd;  /* Light gray grid lines */\n"
"    font: 12px \"Arial\";  /* Font style */\n"
"    selection-background-color: #eaeaea;  /* Light gray selection background */\n"
"    selection-color: #000000;  /* Black text for selected items */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #eeeeee;  /* Light gray header background */\n"
"    color: #333333;  /* Dark gray header text */\n"
"    border: 1px solid #cccccc;  /* Light gray border for headers */\n"
"    padding: 4px;  /* Padding for header text */\n"
"    font: bold 12px \"Arial\";  /* Font style for headers */\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"    background-color: #eeeeee;  /* Light gray corner button */\n"
"    border: 1px solid #cccccc;  /* Border for corner button */\n"
"}")

        self.drawtable = QtWidgets.QWidget(self.centralwidget)
        self.drawtable.setGeometry(430, 200, 915, 481)
        self.drawtable.setStyleSheet("QTableView {\n"
"    background-color: #f7f7f7;  /* Slightly white background */\n"
"    color: #333333;  /* Dark gray text for contrast */\n"
"    border: 2px solid #cccccc;  /* Light gray border */\n"
"    border-radius: 8px;  /* Rounded corners */\n"
"    gridline-color: #dddddd;  /* Light gray grid lines */\n"
"    font: 12px \"Arial\";  /* Font style */\n"
"    selection-background-color: #eaeaea;  /* Light gray selection background */\n"
"    selection-color: #000000;  /* Black text for selected items */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #eeeeee;  /* Light gray header background */\n"
"    color: #333333;  /* Dark gray header text */\n"
"    border: 1px solid #cccccc;  /* Light gray border for headers */\n"
"    padding: 4px;  /* Padding for header text */\n"
"    font: bold 12px \"Arial\";  /* Font style for headers */\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"    background-color: #eeeeee;  /* Light gray corner button */\n"
"    border: 1px solid #cccccc;  /* Border for corner button */\n"
"}")

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        layout = QtWidgets.QVBoxLayout(self.drawtable)
        layout.addWidget(self.canvas)

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("Lattice-Based Algorithm")
 
        self.pushButton.clicked.connect(self.process_encryption) 
    
    def handle_enc(self):
        self.selected_enc = self.comboBox.currentText()
        #self.process_encryption()
        #return selected_enc
        #if selected_enc == "dilithium2":
       #     print('d2')
       # elif selected_enc == "dilithium3":
        #    print('d3')
        #elif selected_enc == "dilithium5":
          #  print('d5')

    def process_encryption(self): 
        message = self.textEdit.toPlainText().strip()
        if not message:
            QtWidgets.QMessageBox.warning(self, "Input Error", "The text area is empty. Please enter a message before encrypting.")
            return
        message = message.encode("utf-8")
        #if self.pushButton.clicked:
        if self.selected_enc == "dilithium2":
            cpu_before = get_cpu_usage()
            start_mem_keygen = get_memory_usage()
            
            start_time = time.time()
            #(public_key, private_key), mem_keygen = measure_memory(lambda: Dilithium2.keygen())
            public_key, private_key= Dilithium2.keygen()
            stop_time = time.time()
            stop_mem_keygen = get_memory_usage()
            
            cpu_after = get_cpu_usage()
            keygen_time_s = stop_time - start_time
            keygen_time = keygen_time_s * 1000
            mem_keygen = stop_mem_keygen - start_mem_keygen
            
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            power_keygen = estimate_power_consumption(cpu_usage, keygen_time_s)
            if mem_keygen == 0:
                mem_keygen = '< 1.00'
            
            
            cpu_before = get_cpu_usage()
            start_mem_sign = get_memory_usage()
            
            start_time = time.time() 
            #signature, mem_sign = measure_memory(Dilithium2.sign(private_key, message))
            signature = Dilithium2.sign(private_key, message)
            sign_time_s = time.time() - start_time 
            
            stop_mem_sign = get_memory_usage()
            cpu_after = get_cpu_usage()
            
            mem_sign = start_mem_sign - start_mem_sign
            sign_time = sign_time_s * 1000
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            power_sign = estimate_power_consumption(cpu_usage, sign_time_s)
            if mem_sign == 0:
                mem_sign = '< 1.00'
            sign_size = len(signature)
            pu_size = len(public_key)
            pr_size = len(private_key)

            cpu_before = get_cpu_usage()
            start_mem_verify = get_memory_usage()
            
            start_verify = time.time() 
            #valid, mem_verify = measure_memory(Dilithium2.verify(public_key, message, signature))
            valid= Dilithium2.verify(public_key, message, signature)
            verify_time_s = time.time() - start_verify 
            cpu_after = get_cpu_usage()
            stop_mem_verify = get_memory_usage()
            
            verify_time = verify_time_s * 1000
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            power_verify = estimate_power_consumption(cpu_usage, verify_time_s)
            
            mem_verify = stop_mem_verify - start_mem_verify
            if mem_verify == 0:
                mem_verify = '< 1.00'

            message_size = len(message) 

        elif self.selected_enc == "dilithium3":
            cpu_before = get_cpu_usage()
            start_mem_keygen = get_memory_usage()
            start_time = time.time()
            #(public_key, private_key), mem_keygen = measure_memory(lambda: Dilithium2.keygen())
            public_key, private_key= Dilithium3.keygen()
            stop_time = time.time()
            stop_mem_keygen = get_memory_usage()
            cpu_after = get_cpu_usage()
            keygen_time_s = stop_time - start_time
            keygen_time = keygen_time_s * 1000
            mem_keygen = stop_mem_keygen - start_mem_keygen
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            power_keygen = estimate_power_consumption(cpu_usage, keygen_time_s)
            if mem_keygen == 0:
                mem_keygen = '< 1.00'
               
            cpu_before = get_cpu_usage()
            start_mem_sign = get_memory_usage()
            start_time = time.time() 
            #signature, mem_sign = measure_memory(Dilithium2.sign(private_key, message))
            signature = Dilithium3.sign(private_key, message)
            sign_time_s = time.time() - start_time 
            
            stop_mem_sign = get_memory_usage()
            cpu_after = get_cpu_usage()
            sign_time = sign_time_s * 1000
            mem_sign = stop_mem_sign - start_mem_sign
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            power_sign = estimate_power_consumption(cpu_usage, sign_time_s)
            if mem_sign == 0:
                mem_sign = '< 1.00'
            sign_size = len(signature)
            pu_size = len(public_key)
            pr_size = len(private_key)

            cpu_before = get_cpu_usage()
            start_mem_verify = get_memory_usage()
            start_verify = time.time() 
            #valid, mem_verify = measure_memory(Dilithium2.verify(public_key, message, signature))
            valid= Dilithium3.verify(public_key, message, signature)
            verify_time_s = time.time() - start_verify 
            cpu_after = get_cpu_usage()
            stop_mem_verify = get_memory_usage()
            verify_time = verify_time_s * 1000
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            power_verify = estimate_power_consumption(cpu_usage, verify_time_s)
            
            mem_verify = stop_mem_verify - start_mem_verify
            if mem_verify == 0:
                mem_verify = '< 1.00'

            message_size = len(message) 

        elif self.selected_enc == "dilithium5":
            cpu_before = get_cpu_usage()
            start_mem_keygen = get_memory_usage()
            start_time = time.time()
            #(public_key, private_key), mem_keygen = measure_memory(lambda: Dilithium2.keygen())
            public_key, private_key= Dilithium5.keygen()
            stop_time = time.time()
            stop_mem_keygen = get_memory_usage()
            cpu_after = get_cpu_usage()
            keygen_time_s = stop_time - start_time
            keygen_time = keygen_time_s * 1000
            mem_keygen = stop_mem_keygen - start_mem_keygen
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            power_keygen = estimate_power_consumption(cpu_usage, keygen_time_s)
            if mem_keygen == 0:
                mem_keygen = '< 1.00'
            
            
            cpu_before = get_cpu_usage()
            start_mem_sign = get_memory_usage()
            start_time = time.time() 
            #signature, mem_sign = measure_memory(Dilithium2.sign(private_key, message))
            signature = Dilithium5.sign(private_key, message)
            sign_time_s = time.time() - start_time 
            
            stop_mem_sign = get_memory_usage()
            cpu_after = get_cpu_usage()
            sign_time = sign_time_s * 1000
            mem_sign = stop_mem_sign - start_mem_sign
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            power_sign = estimate_power_consumption(cpu_usage, sign_time_s)
            if mem_sign == 0:
                mem_sign = '< 1.00'
            sign_size = len(signature)
            pu_size = len(public_key)
            pr_size = len(private_key)

            cpu_before = get_cpu_usage()
            start_mem_verify = get_memory_usage()
            start_verify = time.time() 
            #valid, mem_verify = measure_memory(Dilithium2.verify(public_key, message, signature))
            valid= Dilithium5.verify(public_key, message, signature)
            verify_time_s = time.time() - start_verify 
            cpu_after = get_cpu_usage()
            stop_mem_verify = get_memory_usage()
            verify_time = verify_time_s * 1000
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            power_verify = estimate_power_consumption(cpu_usage, verify_time_s)
            
            mem_verify = stop_mem_verify - start_mem_verify
            if mem_verify == 0:
                mem_verify = '< 1.00'

            message_size = len(message) 
        
        self.ax.clear()
        self.ax.bar(["Sign Time", "Verify Time", "KeyGen Time"], [sign_time, verify_time, keygen_time], color=['red', 'purple', 'gold'])  # Aggressive colors
        self.ax.set_title("Performance of Lattice-Based Cryptography") 
        self.canvas.draw() 

        # Metric and Value Table
        model = QtGui.QStandardItemModel() 
        model.setHorizontalHeaderLabels(["Metric", "Value"])
        model.appendRow([QtGui.QStandardItem("KeyGen Time"), QtGui.QStandardItem(f"{keygen_time:.6f} mS")])  
        model.appendRow([QtGui.QStandardItem("Sign Time"), QtGui.QStandardItem(f"{sign_time:.6f} mS")]) 
        model.appendRow([QtGui.QStandardItem("Verify Time"), QtGui.QStandardItem(f"{verify_time:.6f} mS")]) 
        model.appendRow([QtGui.QStandardItem("Message Size"), QtGui.QStandardItem(f"{message_size} bytes")]) 
        model.appendRow([QtGui.QStandardItem("Signature Validation"), QtGui.QStandardItem("Valid" if valid else "Invalid")]) 
        self.viewtable.setModel(model) 

        header = self.viewtable.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #004080;  /* Dark blue background */
                color: #ffffff;  /* White text */
                font: bold 14px "Arial";
                border: 1px solid #66b3ff;
                padding: 4px;
            }
        """)

        # Key Type and Key Value Table
        view_model = QtGui.QStandardItemModel() 
        view_model.setHorizontalHeaderLabels(["Key Type", "Key Value"]) 
        view_model.appendRow([QtGui.QStandardItem("Public Key"), QtGui.QStandardItem(str(public_key))]) 
        view_model.appendRow([QtGui.QStandardItem("Private Key"), QtGui.QStandardItem(str(private_key))]) 
        view_model.appendRow([QtGui.QStandardItem("Signature"), QtGui.QStandardItem(str(signature))]) 
        view_model.appendRow([QtGui.QStandardItem("Estimated Power\nUsed for KeyGen"), QtGui.QStandardItem(f"{power_keygen:.4f} mJoules")])
        view_model.appendRow([QtGui.QStandardItem("Estimated Power\nUsed for Signing"), QtGui.QStandardItem(f"{power_sign:.4f} mJoules")])
        view_model.appendRow([QtGui.QStandardItem("Estimated Power\nUsed for Verification"), QtGui.QStandardItem(f"{power_verify:.4f} mJoules")])
        view_model.appendRow([QtGui.QStandardItem("Peak Memory Usage\nfor Key Generation"), QtGui.QStandardItem(f"{mem_keygen} KB")]) 
        view_model.appendRow([QtGui.QStandardItem("Peak Memory Usage\nfor Signature"), QtGui.QStandardItem(f"{mem_sign} KB")])
        view_model.appendRow([QtGui.QStandardItem("Peak Memory Usage\nfor Verification"), QtGui.QStandardItem(f"{mem_verify} KB")])
        view_model.appendRow([QtGui.QStandardItem("Public Key Size"), QtGui.QStandardItem(f"{pu_size} byte")]) 
        view_model.appendRow([QtGui.QStandardItem("Private Key Size"), QtGui.QStandardItem(f"{pr_size} byte")]) 
        view_model.appendRow([QtGui.QStandardItem("Signature Size"), QtGui.QStandardItem(f"{sign_size} byte")]) 
        self.encryptiontable.setModel(view_model) 

        # Adjust table header and layout
        self.viewtable.horizontalHeader().setStretchLastSection(True)
        self.viewtable.verticalHeader().setVisible(False)  # Hide vertical header indices
        self.viewtable.setContentsMargins(0, 0, 0, 0)  # Remove extra padding
        self.viewtable.resizeColumnsToContents()
        self.viewtable.resizeRowsToContents()
        self.viewtable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.viewtable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.encryptiontable.horizontalHeader().setStretchLastSection(True)
        self.encryptiontable.verticalHeader().setVisible(False)  # Hide vertical header indices
        self.encryptiontable.setContentsMargins(0, 0, 0, 0)  # Remove extra padding
        self.encryptiontable.resizeColumnsToContents()
        self.encryptiontable.resizeRowsToContents()
        self.encryptiontable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.encryptiontable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        header = self.encryptiontable.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #800000;  /* Dark red background */
                color: #ffffff;  /* White text */
                font: bold 14px "Arial";
                border: 1px solid #ff6666;
                padding: 4px;
            }
        """)

        if self.selected_enc == "dilithium2":
            cpu_before = get_cpu_usage()
            start_mem_sign = get_memory_usage()
            
            start_time = time.time() 
            signature = Dilithium2.sign(private_key, message) 
            sign_time_s = time.time() - start_time 
            cpu_after = get_cpu_usage()
            
            stop_mem_sign = get_memory_usage()
            
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            sign_time = sign_time_s * 1000
            power_sign = estimate_power_consumption(cpu_usage, sign_time_s)
            mem_sign = stop_mem_sign - start_mem_sign
            if mem_sign == 0:
                mem_sign = '< 1.00'
            sign_size = len(signature)
    
            cpu_before = get_cpu_usage()
            start_mem_verify = get_memory_usage()
           
            start_verify = time.time() 
            valid = Dilithium2.verify(public_key, message, signature) 
            verify_time_s = time.time() - start_verify 
            cpu_after = get_cpu_usage()
            
            stop_mem_verify = get_memory_usage()
            
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            verify_time = verify_time_s * 1000
            power_verify = estimate_power_consumption(cpu_usage, verify_time_s)
            mem_verify = stop_mem_verify - start_mem_verify
            if mem_verify == 0:
                mem_verify = '< 1.00'
    
            message_size = len(message) 
 
        if self.selected_enc == "dilithium3":
            cpu_before = get_cpu_usage()
            start_mem_sign = get_memory_usage()
            start_time = time.time() 
            signature = Dilithium3.sign(private_key, message) 
            sign_time_s = time.time() - start_time 
            cpu_after = get_cpu_usage()
            
            stop_mem_sign = get_memory_usage()
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            sign_time = sign_time_s * 1000
            power_sign = estimate_power_consumption(cpu_usage, sign_time_s)
            mem_sign = stop_mem_sign - start_mem_sign
            if mem_sign == 0:
                mem_sign = '< 1.00'
            sign_size = len(signature)
    
            cpu_before = get_cpu_usage()
            start_mem_verify = get_memory_usage()
            start_verify = time.time() 
            valid = Dilithium3.verify(public_key, message, signature) 
            verify_time_s = time.time() - start_verify 
            cpu_after = get_cpu_usage()
            
            stop_mem_verify = get_memory_usage()
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            verify_time = verify_time_s * 1000
            power_verify = estimate_power_consumption(cpu_usage, verify_time_s)
            power_sign = estimate_power_consumption(cpu_usage, sign_time_s)
            mem_verify = stop_mem_verify - start_mem_verify
            if mem_verify == 0:
                mem_verify = '< 1.00'
    
            message_size = len(message) 

        if self.selected_enc == "dilithium5":
            cpu_before = get_cpu_usage()
            start_mem_sign = get_memory_usage()
            start_time = time.time() 
            signature = Dilithium5.sign(private_key, message) 
            sign_time_s = time.time() - start_time 
            cpu_after = get_cpu_usage()
            
            stop_mem_sign = get_memory_usage()
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            sign_time = sign_time_s * 1000
            power_sign = estimate_power_consumption(cpu_usage, sign_time_s)
            mem_sign = stop_mem_sign - start_mem_sign
            if mem_sign == 0:
                mem_sign = '< 1.00'
            sign_size = len(signature)
    
            cpu_before = get_cpu_usage()
            start_mem_verify = get_memory_usage()
            start_verify = time.time() 
            valid = Dilithium5.verify(public_key, message, signature) 
            verify_time_s = time.time() - start_verify 
            cpu_after = get_cpu_usage()
            
            stop_mem_verify = get_memory_usage()
            cpu_usage = cpu_after - cpu_before
            cpu_usage = cpu_usage * 1000
            if cpu_usage < 0:
                cpu_usage = -cpu_usage
            verify_time = verify_time_s * 1000
            power_verify = estimate_power_consumption(cpu_usage, verify_time_s)
            mem_verify = stop_mem_verify - start_mem_verify
            if mem_verify == 0:
                mem_verify = '< 1.00'
    
            message_size = len(message) 
        #def clicked_button(self):
        self.ax.clear() 
        self.ax.bar(["Sign Time", "Verify Time", "KeyGen Time"], [sign_time, verify_time, keygen_time], color=['blue', 'green', 'gold']) 
        for i, v in enumerate([sign_time, verify_time, keygen_time]):
            self.ax.text(i, v + 0.1, f"{v:.2f} mS", ha='center', fontsize=10)
        self.ax.set_title("Performance of Lattice-Based Cryptography") 
        self.canvas.draw() 
 
        model = QtGui.QStandardItemModel() 
        model.setHorizontalHeaderLabels(["Metric", "Value"]) 
        model.appendRow([QtGui.QStandardItem("KeyGen Time"), QtGui.QStandardItem(f"{keygen_time:.6f} mS")]) 
        model.appendRow([QtGui.QStandardItem("Sign Time"), QtGui.QStandardItem(f"{sign_time:.6f} mS")]) 
        model.appendRow([QtGui.QStandardItem("Verify Time"), QtGui.QStandardItem(f"{verify_time:.6f} mS")]) 
        model.appendRow([QtGui.QStandardItem("Message Size"), QtGui.QStandardItem(f"{message_size} bytes")]) 
        model.appendRow([QtGui.QStandardItem("Signature Validation"), QtGui.QStandardItem("Valid" if valid else "Invalid")]) 
        self.viewtable.setModel(model) 
 
        view_model = QtGui.QStandardItemModel() 
        view_model.setHorizontalHeaderLabels(["Key Type", "Key Value"]) 
        view_model.appendRow([QtGui.QStandardItem("Public Key"), QtGui.QStandardItem(str(public_key))]) 
        view_model.appendRow([QtGui.QStandardItem("Private Key"), QtGui.QStandardItem(str(private_key))]) 
        view_model.appendRow([QtGui.QStandardItem("Signature"), QtGui.QStandardItem(str(signature))]) 
        view_model.appendRow([QtGui.QStandardItem("Estimated Power\nUsed for KeyGen"), QtGui.QStandardItem(f"{power_keygen:.4f} mJoules")])
        view_model.appendRow([QtGui.QStandardItem("Estimated Power\nUsed for Signing"), QtGui.QStandardItem(f"{power_sign:.4f} mJoules")])
        view_model.appendRow([QtGui.QStandardItem("Estimated Power\nUsed for Verification"), QtGui.QStandardItem(f"{power_verify:.4f} mJoules")])
        view_model.appendRow([QtGui.QStandardItem("Peak Memory Usage\nfor Key Generation"), QtGui.QStandardItem(f"{mem_keygen} KB")]) 
        view_model.appendRow([QtGui.QStandardItem("Peak Memory Usage\nfor Signature"), QtGui.QStandardItem(f"{mem_sign} KB")])
        view_model.appendRow([QtGui.QStandardItem("Peak Memory Usage\nfor Verification"), QtGui.QStandardItem(f"{mem_verify} KB")])
        view_model.appendRow([QtGui.QStandardItem("Public Key Size"), QtGui.QStandardItem(f"{pu_size} byte")]) 
        view_model.appendRow([QtGui.QStandardItem("Private Key Size"), QtGui.QStandardItem(f"{pr_size} byte")]) 
        view_model.appendRow([QtGui.QStandardItem("Signature Size"), QtGui.QStandardItem(f"{sign_size} byte")]) 
        self.encryptiontable.setModel(view_model) 
 
 
def main(): 
    app = QtWidgets.QApplication(sys.argv) 
    MainWindow = QtWidgets.QMainWindow() 
    ui = MyApp() 
    ui.setupUi(MainWindow) 
    MainWindow.show() 
    sys.exit(app.exec_()) 
 
 
if __name__ == "__main__": 
    main()
