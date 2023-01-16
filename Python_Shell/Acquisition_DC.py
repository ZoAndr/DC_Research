import connect
import parameters
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QCheckBox, QLineEdit

from PyQt5 import QtCore, QtGui

from PyQt5.QtCore import pyqtSlot


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os
import re

import serial
import serial.tools.list_ports
# https://devpress.csdn.net/python/62f614d7c6770329307fbd8d.html

from c_Thread import *


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('SVG')

import random

import numpy as np

from datetime import datetime


class Example(QWidget):
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.COMM = serial.Serial()

        self.connected = False
        
        self.COMM_Port = 'XXX'

        self.thread1 = threading.Thread(target=self.thread_com_receive)
        self.thread_started = False

        self.rx_buf = ''
        self.Head = 0
        self.Tail = 0
        self.U_inp = 0
        self.I_inp = 0
        self.U_out = 0
        self.I_out = 0
        self.t_1 = 0
        self.t_2 = 0
        self.t_3 = 0

        self.U_unit_1st_bit = 0.5
        self.U_unit_2nd_bit = 0.0025
        self.I_unit_1st_bit = 0.1
        self.I_unit_2nd_bit = 0.0005
        self.t_unit_1st_bit = 1
        self.t_unit_2nd_bit = 0.01

#        self.t_Seed    =  5
#        self.t_Period  = 20
#        self.t_Strobe  =  3
#        self.t_Delay   = 12
#        self.t_Active  =  4
#        self.t_ADC     = 10
#        self.N_Periods =  3
#        self.N_ADC_steps = 50
#        self.N_ADC_mpy = 10

        self.t_Period  = 20000
        self.t_Strobe  =  11
        self.t_Delay   =  30
        self.t_Active  =  40
        self.t_ADC     =  5
        self.N_Periods =  1
        self.N_ADC_steps = 1000

        self.time_ADC = np.arange(0, self.N_ADC_steps)

        self.N_Graph = 2000
        self.grph_pntr = 0
        self.U_inp_Grph = np.zeros(self.N_Graph)
        self.I_inp_Grph = np.zeros(self.N_Graph)
        self.U_out_Grph = np.zeros(self.N_Graph)
        self.I_out_Grph = np.zeros(self.N_Graph)
        self.t_001_Grph = np.zeros(self.N_Graph)
        self.t_002_Grph = np.zeros(self.N_Graph)
        self.t_003_Grph = np.zeros(self.N_Graph)

        self.P_inp = np.zeros(self.N_Graph)
        self.P_out = np.zeros(self.N_Graph)
        self.Rat   = np.zeros(self.N_Graph)


        self.CHK_Bx_Uin  = True
        self.CHK_Bx_Iin  = True
        self.CHK_Bx_Uout = True
        self.CHK_Bx_Iout = True
        self.CHK_Bx_T1   = True
        self.CHK_Bx_T2   = True
        self.CHK_Bx_T3   = True
        self.CHK_Bx_Pwr  = True
        self.CHK_Bx_Rat  = True

#        combo.activated[str].connect(self.onChanged)     

        self.Create_Elements()
        self.Place_Elements()        
         


        self.setGeometry(50,50,1550,800)
        self.setWindowTitle("QLineEdit Example")
        self.show()

    def Create_Elements(self):
        global portinfo
        portinfo = connect.getOpenPorts()

        # COMM Port selection ComboBox        
        self.COMM_select  = QComboBox(self)
        self.COMM_Update         = QPushButton('Ports state Upd', self)
        self.COMM_Connect        = QPushButton('Pump Connect', self)

        self.Send_Prmtrs        = QPushButton('Send_Parameters', self)


        self.Measurement_Values_1    = QLabel('U_in I_in ', self)
        self.Measurement_Values_1.setFont(QFont('Arial', 18))
        self.Measurement_Values_2    = QLabel('U_out I_out', self)
        self.Measurement_Values_2.setFont(QFont('Arial', 18))
        self.Measurement_Values_3    = QLabel('t_1 t_1 t_3', self)
        self.Measurement_Values_3.setFont(QFont('Arial', 18))
                       
        # Parameters for sending
        self.Edit_t_Period    =  QLineEdit(str(self.t_Period   ), self)
        self.Edit_t_Strobe    =  QLineEdit(str(self.t_Strobe   ), self)
        self.Edit_t_Delay     =  QLineEdit(str(self.t_Delay    ), self)
        self.Edit_t_Active    =  QLineEdit(str(self.t_Active   ), self)
        self.Edit_t_ADC       =  QLineEdit(str(self.t_ADC      ), self)
        self.Edit_N_Periods   =  QLineEdit(str(self.N_Periods  ), self)
        self.Edit_N_ADC_steps =  QLineEdit(str(self.N_ADC_steps), self)

        self.t_Period_txt    = QLabel('t_Period', self)
        self.t_Period_txt.setFont(QFont('Arial', 8))
        self.t_Strobe_txt    = QLabel('t_Strobe', self)
        self.t_Strobe_txt.setFont(QFont('Arial', 8))
        self.t_Delay_txt    = QLabel('t_Delay', self)
        self.t_Delay_txt.setFont(QFont('Arial', 8))
        self.t_Active_txt    = QLabel('t_Active', self)
        self.t_Active_txt.setFont(QFont('Arial', 8))
        self.t_ADC_txt    = QLabel('t_ADC', self)
        self.t_ADC_txt.setFont(QFont('Arial', 8))
        self.N_Periods_txt    = QLabel('N_Periods', self)
        self.N_Periods_txt.setFont(QFont('Arial', 8))
        self.N_ADC_steps_txt    = QLabel('N_ADC_steps', self)
        self.N_ADC_steps_txt.setFont(QFont('Arial', 8))

        self.checkBox_Uin = QCheckBox('U in', self)
        self.checkBox_Uin.setChecked(True)
        self.checkBox_Uin.stateChanged.connect(self.checked_Box_Uin)
        self.checkBox_Iin = QCheckBox('I in', self)
        self.checkBox_Iin.setChecked(True)
        self.checkBox_Iin.stateChanged.connect(self.checked_Box_Iin)
        self.checkBox_Uout = QCheckBox('U out', self)
        self.checkBox_Uout.setChecked(True)
        self.checkBox_Uout.stateChanged.connect(self.checked_Box_Uout)
        self.checkBox_Iout = QCheckBox('I out', self)
        self.checkBox_Iout.setChecked(True)
        self.checkBox_Iout.stateChanged.connect(self.checked_Box_Iout)

        self.checkBox_T1 = QCheckBox('t1, oC', self)
        self.checkBox_T1.setChecked(True)
        self.checkBox_T1.stateChanged.connect(self.checked_Box_T1)
        self.checkBox_T2 = QCheckBox('t2, oC', self)
        self.checkBox_T2.setChecked(True)
        self.checkBox_T2.stateChanged.connect(self.checked_Box_T2)
        self.checkBox_T3 = QCheckBox('t3, oC', self)
        self.checkBox_T3.setChecked(True)
        self.checkBox_T3.stateChanged.connect(self.checked_Box_T3)

        self.checkBox_Pwr = QCheckBox('Pwr', self)
        self.checkBox_Pwr.setChecked(True)
        self.checkBox_Pwr.stateChanged.connect(self.checked_Box_Pwr)
        self.checkBox_Rat = QCheckBox('K ratio', self)
        self.checkBox_Rat.setChecked(True)
        self.checkBox_Rat.stateChanged.connect(self.checked_Box_Rat)

        self.Save_FileBttn = QPushButton('Save file', self)
        self.Save_FileName = QLineEdit('Save_File_Name', self)
#=========================================================================        
        for port in portinfo:
            self.COMM_select.addItem(port)

        self.COMM_select.activated[str].connect(self.click_COMM_select)
        self.COMM_Update.clicked.connect(self.click_COMM_Update)
        self.COMM_Connect.clicked.connect(self.click_COMM_Connect)
        self.COMM_Connect.setEnabled(False)
        self.Send_Prmtrs.setEnabled(False)
        self.Save_FileBttn.setEnabled(False)

        self.Send_Prmtrs.clicked.connect(self.Create_Pack_from_Parameters)
        self.Save_FileBttn.clicked.connect(self.fnk_Save_File)
        
#        self.myConnection = connect.Connection(port=self.COMM_Port,
#                                               baudrate='9600', x='Single Pump', mode=1)


    def checked_Box_Uin(self, checked):
        if checked:
            self.CHK_Bx_Uin = True
        else:
            self.CHK_Bx_Uin = False
        self.show()

    def checked_Box_Iin(self, checked):
        if checked:
            self.CHK_Bx_Iin = True
        else:
            self.CHK_Bx_Iin = False
        self.show()

    def checked_Box_Uout(self, checked):
        if checked:
            self.CHK_Bx_Uout = True
        else:
            self.CHK_Bx_Uout = False
        self.show()

    def checked_Box_Iout(self, checked):
        if checked:
            self.CHK_Bx_Iout = True
        else:
            self.CHK_Bx_Iout = False
        self.show()

    def checked_Box_T1(self, checked):
        if checked:
            self.CHK_Bx_T1 = True
        else:
            self.CHK_Bx_T1 = False
        self.show()

    def checked_Box_T2(self, checked):
        if checked:
            self.CHK_Bx_T2 = True
        else:
            self.CHK_Bx_T2 = False
        self.show()

    def checked_Box_T3(self, checked):
        if checked:
            self.CHK_Bx_T3 = True
        else:
            self.CHK_Bx_T3 = False
        self.show()

    def checked_Box_Pwr(self, checked):
        if checked:
            self.CHK_Bx_Pwr = True
        else:
            self.CHK_Bx_Pwr = False
        self.show()

    def checked_Box_Rat(self, checked):
        if checked:
            self.CHK_Bx_Rat = True
        else:
            self.CHK_Bx_Rat = False
        self.show()

     


    def Check_Comm_Settings(self):

        if self.COMM_Port[0] == 'C':
            print('It is possible to try to open Comm Port')
            self.COMM_Connect.setEnabled(True)
            self.Send_Prmtrs.setEnabled(True)
                
                

       

    def Place_Elements(self):
        self.COMM_select.move(20, 35)
        self.COMM_Update.move(20, 10)
        self.COMM_Connect.setGeometry(105, 10, 100, 45)
        
        self.Measurement_Values_1.setGeometry(840, 25, 490, 40)
        self.Measurement_Values_2.setGeometry(840, 55, 420, 40)
        self.Measurement_Values_3.setGeometry(840, 85, 540, 40)

        X_strt = 25; X_step = 80
        Y_strt = 60; Y_step = 80

        self.Edit_t_Period.setGeometry(   X_strt +  0 * X_step, Y_strt + 25, 40, 40)
        self.Edit_t_Strobe.setGeometry(   X_strt +  1 * X_step, Y_strt + 25, 40, 40)
        self.Edit_t_Delay.setGeometry(    X_strt +  2 * X_step, Y_strt + 25, 40, 40)
        self.Edit_t_Active.setGeometry(   X_strt +  3 * X_step, Y_strt + 25, 40, 40)
        self.Edit_t_ADC.setGeometry(      X_strt +  4 * X_step, Y_strt + 25, 40, 40)
        self.Edit_N_Periods.setGeometry(  X_strt +  5 * X_step, Y_strt + 25, 40, 40)
        self.Edit_N_ADC_steps.setGeometry(X_strt +  6 * X_step, Y_strt + 25, 40, 40)

        self.t_Period_txt.setGeometry(   X_strt +  0 * X_step, Y_strt + 5, 70, 15)
        self.t_Strobe_txt.setGeometry(   X_strt +  1 * X_step, Y_strt + 5, 70, 15)
        self.t_Delay_txt.setGeometry(    X_strt +  2 * X_step, Y_strt + 5, 70, 15)
        self.t_Active_txt.setGeometry(   X_strt +  3 * X_step, Y_strt + 5, 70, 15)
        self.t_ADC_txt.setGeometry(      X_strt +  4 * X_step, Y_strt + 5, 70, 15)
        self.N_Periods_txt.setGeometry(  X_strt +  5 * X_step, Y_strt + 5, 70, 15)
        self.N_ADC_steps_txt.setGeometry(X_strt +  6 * X_step, Y_strt + 5, 70, 15)

        Y_strt2 = 60; Y_step2 = 25
        self.checkBox_Uin.setGeometry(QtCore.QRect( 1100, Y_strt2 + 0 * Y_step2, 87, 20))
        self.checkBox_Iin.setGeometry(QtCore.QRect( 1100, Y_strt2 + 1 * Y_step2, 87, 20))
        self.checkBox_Uout.setGeometry(QtCore.QRect(1100, Y_strt2 + 2 * Y_step2, 87, 20))
        self.checkBox_Iout.setGeometry(QtCore.QRect(1100, Y_strt2 + 3 * Y_step2, 87, 20))
        self.checkBox_T1.setGeometry(QtCore.QRect(  1100, Y_strt2 + 4 * Y_step2, 87, 20))
        self.checkBox_T2.setGeometry(QtCore.QRect(  1100, Y_strt2 + 5 * Y_step2, 87, 20))
        self.checkBox_T3.setGeometry(QtCore.QRect(  1100, Y_strt2 + 6 * Y_step2, 87, 20))
        self.checkBox_Pwr.setGeometry(QtCore.QRect(  1100, Y_strt2 + 7 * Y_step2, 87, 20))
        self.checkBox_Rat.setGeometry(QtCore.QRect(  1100, Y_strt2 + 8 * Y_step2, 87, 20))

        self.Save_FileName.setGeometry(QtCore.QRect(  1200, Y_strt2 + 4 * Y_step2, 200, 50))
        self.Save_FileBttn.setGeometry(QtCore.QRect(  1420, Y_strt2 + 4 * Y_step2 + 10, 100, 30))

        self.Send_Prmtrs.setGeometry(  int(7.5 * X_step), 90, 110, 35)


        self.plot_widget_In = QWidget(self)
        self.plot_widget_In.setGeometry(20,150,500,320)
        self.figure_In = plt.figure()
        self.plotting_In = FigureCanvas(self.figure_In)
        plot_box_In = QVBoxLayout()
        plot_box_In.addWidget(self.plotting_In)
        self.plot_widget_In.setLayout(plot_box_In)

        self.plot_widget_Out = QWidget(self)
        self.plot_widget_Out.setGeometry(520,150,500,320)
        self.figure_Out = plt.figure()
        self.plotting_Out = FigureCanvas(self.figure_Out)
#        self.plot()
        plot_box_Out = QVBoxLayout()
        plot_box_Out.addWidget(self.plotting_Out)
        self.plot_widget_Out.setLayout(plot_box_Out)

        self.plot_widget_Pwr = QWidget(self)
        self.plot_widget_Pwr.setGeometry(1020,310,500,320)
        self.figure_Pwr = plt.figure()
        self.plotting_Pwr = FigureCanvas(self.figure_Pwr)
#        self.plot()
        plot_box_Pwr = QVBoxLayout()
        plot_box_Pwr.addWidget(self.plotting_Pwr)
        self.plot_widget_Pwr.setLayout(plot_box_Pwr)

        self.plot_widget_T12 = QWidget(self)
        self.plot_widget_T12.setGeometry(20,470,500,320)
        self.figure_T12 = plt.figure()
        self.plotting_T12 = FigureCanvas(self.figure_T12)
#        self.plot()
        plot_box_T12 = QVBoxLayout()
        plot_box_T12.addWidget(self.plotting_T12)
        self.plot_widget_T12.setLayout(plot_box_T12)

        self.plot_widget_T3 = QWidget(self)
        self.plot_widget_T3.setGeometry(520,470,500,320)
        self.figure_T3 = plt.figure()
        self.plotting_T3 = FigureCanvas(self.figure_T3)
#        self.plot()
        plot_box_T3 = QVBoxLayout()
        plot_box_T3.addWidget(self.plotting_T3)
        self.plot_widget_T3.setLayout(plot_box_T3)



    def plot(self):
        ''' plot some random stuff '''
        data = [random.random() for i in range(10)]
        self.ax_In = self.figure_In.add_subplot(111)
        self.ax_In.hold(False)
        self.ax_In.plot(data, '*-')
        self.plotting_In.draw()


    def click_COMM_select(self, text):

        self.COMM_Port = text
        print(self.COMM_Port)
        self.Check_Comm_Settings()
            
    @pyqtSlot()
    def click_COMM_Update(self):
        portinfo = connect.getOpenPorts()
        self.COMM_select.clear()
        for port in portinfo:
            self.COMM_select.addItem(port)
        print('PyQt5 button click')

#        open_file()

    def click_BaudRate_Sel(self, text):
        global BaudRate
        self.BaudRate = text
        self.Check_Comm_Settings()
        


    @pyqtSlot()
    def click_COMM_Connect(self):
        if not self.connected:
            try:
                self.COMM = serial.Serial(self.COMM_Port, 115200, timeout=0.01)
                if self.COMM.isOpen():
                    print(self.COMM_Port, " open success")
                    self.connected = False
                    self.COMM_Connect.setText("Disconnect")
                    self.connected = True
                    self.COMM_select.setEnabled(False)
                    self.COMM_Update.setEnabled(False)
                    self.Comm_Port_opened_successfully = True
    
                    if(self.thread_started == False):
                        self.thread_started = True
                        self.thread1.start()
                    return 0
                else:
                    print("open failed")
                    return 255


            except TypeError as e:
                print(e)
                self.Comm_Port_opened_successfully = False
#                self.check_Auto_pH_Control_Possible()
        else:
            self.COMM.close()
#            self.connectLbl.setText("Disconnected")
            self.COMM_Connect.setText("Board Connect")
            self.connected = False
#            self.connected = False
            self.COMM_select.setEnabled(True)
            self.COMM_Update.setEnabled(True)
            self.Comm_Port_opened_successfully = False
            

    def process_inbox(self):

        N = len(self.rx_buf)
        k = 0
        received = ''
        while(k < N):
            if((self.rx_buf[k] == 255) & (N - k >= 16)):
                self.U_inp = int(self.rx_buf[k + 1])  * self.U_unit_1st_bit + int(self.rx_buf[k + 2]) * self.U_unit_2nd_bit
                self.I_inp = int(self.rx_buf[k + 3])  * self.I_unit_1st_bit + int(self.rx_buf[k + 4]) * self.I_unit_2nd_bit
                self.U_out = int(self.rx_buf[k + 5])  * self.U_unit_1st_bit + int(self.rx_buf[k + 6]) * self.U_unit_2nd_bit
                self.I_out = int(self.rx_buf[k + 7])  * self.I_unit_1st_bit + int(self.rx_buf[k + 8]) * self.I_unit_2nd_bit
                self.t_1   = int(self.rx_buf[k + 9])  * self.t_unit_1st_bit + int(self.rx_buf[k + 10]) * self.t_unit_2nd_bit
                self.t_2   = int(self.rx_buf[k + 11]) * self.t_unit_1st_bit + int(self.rx_buf[k + 12]) * self.t_unit_2nd_bit
                self.t_3   = int(self.rx_buf[k + 13]) * self.t_unit_1st_bit + int(self.rx_buf[k + 14]) * self.t_unit_2nd_bit
                received = received + str(round(self.U_inp, 2)) + ' ' + str(round(self.I_inp, 2)) + ' ' \
                                    + str(round(self.U_out, 2)) + ' ' + str(round(self.I_out, 2)) + ' ' \
                                    + str(round(self.t_1, 2)) + ' ' + str(round(self.t_2, 2)) + ' ' + str(round(self.t_3, 2)) + '\n' 

                self.U_inp_Grph[self.grph_pntr] = self.U_inp
                self.I_inp_Grph[self.grph_pntr] = self.I_inp
                self.U_out_Grph[self.grph_pntr] = self.U_out
                self.I_out_Grph[self.grph_pntr] = self.I_out
                self.t_001_Grph[self.grph_pntr] = self.t_1
                self.t_002_Grph[self.grph_pntr] = self.t_2
                self.t_003_Grph[self.grph_pntr] = self.t_3
                self.grph_pntr = self.grph_pntr + 1

                
                if(int(self.rx_buf[k + 15]) == 253):
                    self.grph_pntr = 0
                    self.time_ADC = np.arange(0, self.N_ADC_steps)

                    self.figure_In.clear()
                    self.figure_Out.clear()
                    self.figure_T12.clear()
                    self.figure_T3.clear()
                    self.figure_Pwr.clear()

                    if(self.CHK_Bx_Uin | self.CHK_Bx_Iin):
                        self.ax_In = self.figure_In.add_subplot(111)
                        if(self.CHK_Bx_Uin):
                            self.ax_In.plot(self.time_ADC, self.U_inp_Grph[0: self.N_ADC_steps], '-', label = 'U_in')
                        if(self.CHK_Bx_Iin):
                            self.ax_In.plot(self.time_ADC, self.I_inp_Grph[0: self.N_ADC_steps], '-', label = 'I_in')
                        self.figure_In.legend()
                    self.plotting_In.draw()

                    if(self.CHK_Bx_Uout | self.CHK_Bx_Iout):
                        self.ax_Out = self.figure_Out.add_subplot(111)
                        if(self.CHK_Bx_Uout):
                            self.ax_Out.plot(self.time_ADC, self.U_out_Grph[0: self.N_ADC_steps], '-', label = 'Uout')
                        if(self.CHK_Bx_Iout):
                            self.ax_Out.plot(self.time_ADC, self.I_out_Grph[0: self.N_ADC_steps], '-', label = 'Iout')
                        self.figure_Out.legend()
                    self.plotting_Out.draw()

                    if(self.CHK_Bx_T1 | self.CHK_Bx_T2):
                        self.ax_Out = self.figure_T12.add_subplot(111)
                        if(self.CHK_Bx_T1):
                            self.ax_Out.plot(self.time_ADC, self.t_001_Grph[0: self.N_ADC_steps], '-', label = 't1,oC')
                        if(self.CHK_Bx_T2):
                            self.ax_Out.plot(self.time_ADC, self.t_002_Grph[0: self.N_ADC_steps], '-', label = 't2,oC')
                        self.figure_T12.legend()
                    self.plotting_T12.draw()

                    if(self.CHK_Bx_T3):
                        self.ax_Out = self.figure_T3.add_subplot(111)
                        self.ax_Out.plot(self.time_ADC, self.t_003_Grph[0: self.N_ADC_steps], '-', label = 't3,oC')
                        self.figure_T3.legend()
                    self.plotting_T3.draw()

                    self.P_inp = np.multiply(self.U_inp_Grph[0: self.N_ADC_steps], self.I_inp_Grph[0: self.N_ADC_steps])
                    self.P_out = np.multiply(self.U_out_Grph[0: self.N_ADC_steps], self.I_out_Grph[0: self.N_ADC_steps])
                    self.Rat = np.divide(self.P_out, self.P_inp) * 100

                    if(self.CHK_Bx_Pwr | self.CHK_Bx_Rat):
                        self.ax_Out = self.figure_Pwr.add_subplot(111)
                        if(self.CHK_Bx_Pwr):
                            self.ax_Out.plot(self.time_ADC, self.P_inp, '-', label = 'P in')
                            self.ax_Out.plot(self.time_ADC, self.P_out, '-', label = 'P out')
                        if(self.CHK_Bx_Rat):
                            
                            self.ax_Out.plot(self.time_ADC, self.Rat, '-', label = 'K ratio')
                        self.figure_Pwr.legend()
                    self.plotting_Pwr.draw()
#                    self.rx_buf = self.rx_buf[k: N]

                self.Save_FileBttn.setEnabled(True)
                k = k + 16

        return received

    def convert_RxBuf_to_Var(self):
        self.Head = self.rx_buf[0]
        self.Tail = self.rx_buf[15]
        self.U_inp = int(self.rx_buf[1])  * self.U_unit_1st_bit + int(self.rx_buf[2]) * self.U_unit_2nd_bit
        self.I_inp = int(self.rx_buf[3])  * self.I_unit_1st_bit + int(self.rx_buf[4]) * self.I_unit_2nd_bit
        self.U_out = int(self.rx_buf[5])  * self.U_unit_1st_bit + int(self.rx_buf[6]) * self.U_unit_2nd_bit
        self.I_out = int(self.rx_buf[7])  * self.I_unit_1st_bit + int(self.rx_buf[8]) * self.I_unit_2nd_bit
        self.t_1   = int(self.rx_buf[9])  * self.t_unit_1st_bit + int(self.rx_buf[10]) * self.t_unit_2nd_bit
        self.t_2   = int(self.rx_buf[11]) * self.t_unit_1st_bit + int(self.rx_buf[12]) * self.t_unit_2nd_bit
        self.t_3   = int(self.rx_buf[13]) * self.t_unit_1st_bit + int(self.rx_buf[14]) * self.t_unit_2nd_bit

    def fnk_Save_File(self):
        with open(self.Save_FileName.text() + '.txt', 'w') as f:
            for k in range(0, self.N_ADC_steps):
                line = str(round(self.U_inp_Grph[k], 2)) + ' ' + str(round(self.I_inp_Grph[k], 2)) + ' ' +\
                    str(round(self.U_out_Grph[k], 2)) + ' ' + str(round(self.I_out_Grph[k], 2)) + ' ' +\
                    str(round(self.t_001_Grph[k], 2)) + ' ' + str(round(self.t_002_Grph[k], 2)) +  ' ' + str(round(self.t_003_Grph[k], 2)) + ' ' +\
                    str(round(self.P_inp[k], 2)) + ' ' + str(round(self.P_out[k], 2)) +  ' ' + str(round(self.Rat[k], 2)) + '\n'
                f.writelines(line)


    def Create_Pack_from_Parameters(self):

        self.t_Period  = int( self.Edit_t_Period.text() )
        self.t_Strobe  = int( self.Edit_t_Strobe.text() )
        self.t_Delay   = int( self.Edit_t_Delay.text() )
        self.t_Active  = int( self.Edit_t_Active.text() )
        self.t_ADC     = int( self.Edit_t_ADC.text() )
        self.N_Periods = int( self.Edit_N_Periods.text() )
        self.N_ADC_steps = int( self.Edit_N_ADC_steps.text() )

        Period_H    = int(self.t_Period / 250)
        Period_L    = (self.t_Period - Period_H * 250)
        Strobe_H    = int(self.t_Strobe / 250)
        Strobe_L    = (self.t_Strobe - Strobe_H * 250)
        Delay_H     = int(self.t_Delay / 250)
        Delay_L     = (self.t_Delay - Delay_H * 250)
        Active_H    = int(self.t_Active / 250)
        Active_L    = (self.t_Active - Active_H * 250)
        ADC_H       = int(self.t_ADC / 250)
        ADC_L       = (self.t_ADC - ADC_H * 250)
        N_Periods_H = int(self.N_Periods / 250)
        N_Periods_L = (self.N_Periods - N_Periods_H * 250)
        ADC_taps_H  = int(self.N_ADC_steps / 250)
        ADC_taps_L  = (self.N_ADC_steps - ADC_taps_H * 250)

#        TX_Buf = (chr)(255) + (chr)(self.t_Seed) + \
#        TX_Buf = '\xff' + \
#            self.t_Seed.to_bytes(8, 'big') + \
#            self.t_Period.to_bytes(8, 'big')
#       + \
#        integer_val.to_bytes((self.t_Strobe), 'big') + \
#        integer_val.to_bytes((self.t_Delay), 'big') + \
#        integer_val.to_bytes((self.t_Active), 'big') + \
#        integer_val.to_bytes((self.t_ADC), 'big') + \
#        integer_val.to_bytes((self.N_Periods), 'big') + \
#        integer_val.to_bytes((N_ADC_Coded), 'big') + '\xfe'

        TX_Buf = bytearray([255, Period_H, Period_L, Strobe_H, Strobe_L, Delay_H, \
                                 Delay_L, Active_H, Active_L, ADC_H, ADC_L, N_Periods_H, \
                                 N_Periods_L, ADC_taps_H, ADC_taps_L, 254])

        print(TX_Buf)                     

#        response = self.sendCommand(TX_Buf)

#        arg = bytes(str(TX_Buf), 'utf8') + b'\r'
        self.COMM.write(TX_Buf)
        
    def thread_com_receive(self):
        while True:
            try:
                self.rx_buf = ''
                self.rx_buf = self.COMM.read()  # Convert to integer number
                if self.rx_buf != b'':
                    self.rx_buf = self.rx_buf + self.COMM.read_all()
#                    print("Serial port receives message:", rx_buf)

                    A = self.process_inbox()

#                    self.convert_RxBuf_to_Var()
#                    print(self.Head)
#                    print(self.Tail)
#                    print('U_in = ',  str(round(self.U_inp, 2)), 'V, I_in = ', str(round(self.I_inp, 2)), 'A')
#                    print('U_out = ', str(round(self.U_out, 2)), 'V, I_out = ', str(round(self.I_out, 2)), 'A')
#                    print('t_1 = ',   str(round(self.t_1, 2)), 'oC, t_2 = ',   str(round(self.t_2, 2)), 'oC, t_3 = ', str(self.t_3), 'oC')
#
#                    self.Measurement_Values_1.setText('U_in = ' +  str(round(self.U_inp, 2))+ 'V, I_in = '+ str(round(self.I_inp, 2))+ 'A')
#                    self.Measurement_Values_2.setText('U_out = '+ str(round(self.U_out, 2))+ 'V, I_out = '+ str(round(self.I_out, 2))+ 'A')
#                    self.Measurement_Values_3.setText('t_1 = '+   str(round(self.t_1, 2))+ 'oC, t_2 = '+   str(round(self.t_2, 2))+ 'oC, t_3 = '+ str(self.t_3)+ 'oC')
#                    self.show()

                    time.sleep(0.1)
                time.sleep(0.1)
            except:
                pass
        pass
   

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    

   
    
    ex = Example()
    sys.exit(app.exec_())

#https://www.pythonguis.com/tutorials/plotting-matplotlib/
