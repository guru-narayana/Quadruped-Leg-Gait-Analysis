#!/usr/bin/env python3

import tkinter as tk
from tkinter import *
import time
import numpy as np
import pandas
import odrive
from odrive.enums import *

odrv0 = odrive.find_any()
axis  = odrv0.axis0
axis.requested_state = AXIS_STATE_IDLE

if(odrv0.vbus_voltage<22):
    print("Vbus voltage is too low. Please check the connection.")
    exit()
else:
    print("Vbus voltage is ok")


data = []
class gui:


    def __init__(self):
        self.root = Tk()
        self.root.title("Odrive Tuning")
        
        self.root.geometry("720x720")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW",self.on_closing) 
        
        self.app = Frame(self.root, bg="white")
        self.app.place(x=738,y=20,in_=self.root)
        self.lmain = Label(self.app)
        self.lmain.grid()

        self.button_caliberate = Button(self.root,text = "caliberate",command = self.caliberate,width=15,bg="#DCDCDC")
        self.button_caliberate.place(x = 70,y = 670)



        self.button_save_config = Button(self.root,text = "save_config",command = self.save_config,width=15,bg="#DCDCDC")
        self.button_save_config.place(x = 270,y = 670)
        
        self.button_closeloop = Button(self.root,text = "pos cntrl",command = self.closeloop,width=15,bg="#DCDCDC")
        self.button_closeloop.place(x = 500,y = 150)
        self.Tkinter_pos_setpoint = StringVar()
        self.Tkinter_pos_setpoint.set(str(axis.encoder.pos_estimate))

        self.Tkinter_pos_gain = StringVar()
        self.Tkinter_vel_gain = StringVar()
        self.Tkinter_vel_integrator_gain = StringVar()
        self.Tkinter_Current_status = StringVar()
        self.Tkinter_POS_status = StringVar()
        self.Tkinter_Weight_status = StringVar()



        self.Tkinter_pos_gain.set(str(axis.controller.config.pos_gain))
        self.Tkinter_vel_gain.set(str(axis.controller.config.vel_gain))
        self.Tkinter_vel_integrator_gain.set(str(axis.controller.config.vel_integrator_gain))
        self.Tkinter_Current_status.set(str(round(axis.motor.current_control.Iq_setpoint,2)))
        self.Tkinter_POS_status.set(str(round(axis.encoder.pos_estimate,2)))
        self.Tkinter_Weight_status.set(str(0))



        label1 =   tk.Label(self.root, text="Pos Gain")
        label1.place(x = 20,y = 10)
        self.pos_gain_entry = tk.Entry(self.root,textvariable = self.Tkinter_pos_gain, font=('calibre',10,'normal'))
        self.pos_gain_entry.place(x = 100,y = 10)
        self.setgain1_button = Button(self.root,text = "set",command = self.setgain1,width=5,height=1,bg="#DCDCDC")
        self.setgain1_button.place(x = 300,y = 8)

        label2 =   tk.Label(self.root, text="Vel Gain")
        label2.place(x = 20,y = 50)
        self.Vel_gain_entry = tk.Entry(self.root,textvariable = self.Tkinter_vel_gain, font=('calibre',10,'normal'))
        self.Vel_gain_entry.place(x = 100,y = 50)
        self.setgain2_button = Button(self.root,text = "set",command = self.setgain2,width=5,height=1,bg="#DCDCDC")
        self.setgain2_button.place(x = 300,y = 45)

        label3 =   tk.Label(self.root, text="Vel Int Gain")
        label3.place(x = 5,y = 90)
        self.Vel_Int_gain_entry = tk.Entry(self.root,textvariable = self.Tkinter_vel_integrator_gain, font=('calibre',10,'normal'))
        self.Vel_Int_gain_entry.place(x = 100,y = 90)
        self.setgain3_button = Button(self.root,text = "set",command = self.setgain3,width=5,height=1,bg="#DCDCDC")
        self.setgain3_button.place(x = 300,y = 85)

        self.Current_status_label = tk.Label(self.root, text="Measured Current (I)   = ")
        self.Current_status_label.place(x = 5,y = 190)

        self.Current_status_entry = tk.Entry(self.root,textvariable = self.Tkinter_Current_status, font=('calibre',10,'normal'))
        self.Current_status_entry.place(x = 170,y = 190)

        self.POS_status_label = tk.Label(self.root, text=    "Measured Pos (Turns) = ")
        self.POS_status_label.place(x = 5,y = 230)

        self.POS_status_entry = tk.Entry(self.root,textvariable = self.Tkinter_POS_status, font=('calibre',10,'normal'))
        self.POS_status_entry.place(x = 170,y = 230)

        self.POS_status_label = tk.Label(self.root, text=    "Mass (gm)                   = ")
        self.POS_status_label.place(x = 5,y = 270)

        self.Weight_status_entry = tk.Entry(self.root,textvariable = self.Tkinter_Weight_status, font=('calibre',10,'normal'))
        self.Weight_status_entry.place(x = 170,y = 270)


        self.button_add_data = Button(self.root,text = "Add_data",command = self.add_data,width=12,bg="#DCDCDC")
        self.button_add_data.place(x = 10,y = 320)

        self.button_save_data = Button(self.root,text = "save_data",command = self.save_data,width=12,bg="#DCDCDC")
        self.button_save_data.place(x = 190,y = 320)
    
    def add_data(self):
        d = [round(axis.motor.current_control.Iq_setpoint,2),round(axis.encoder.pos_estimate,2),float(self.Tkinter_Weight_status.get())+75.0]
        data.append(d)
        print(data)
    def save_data(self):
        df = pandas.DataFrame(data, columns =['Current', 'Position', 'Weight'], dtype = float)
        df.to_excel("Data.xlsx")
    def save_config(self):
        odrv0.save_configuration()
        time.sleep(3)
        odrv0 = odrive.find_any()
        axis  = odrv0.axis0

    def setgain1(self):
        axis.controller.config.pos_gain = float(self.Tkinter_pos_gain.get())
    def setgain2(self):
        axis.controller.config.vel_gain = float(self.Tkinter_vel_gain.get())
    def setgain3(self):
        axis.controller.config.vel_integrator_gain = float(self.Tkinter_vel_integrator_gain.get())

    def caliberate(self):
        axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        time.sleep(15)
        axis.requested_state = AXIS_STATE_IDLE

    def closeloop(self):
        axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL   
        self.button_cancelloop = Button(self.root,text = "cancel",command = self.cancelloop,width=15,bg="#DCDCDC")
        self.button_cancelloop.place(x = 500,y = 150) 
        self.setpos = tk.Entry(self.root,textvariable = self.Tkinter_pos_setpoint, font=('calibre',10,'normal'))
        self.setpos.place(x = 496,y = 50)
        self.button_setpos = Button(self.root,text = "set",command = setpos,width=15,bg="#DCDCDC")
        self.button_setpos.place(x = 500,y = 100)
        self.button_closeloop.destroy()
       
    def cancelloop(self):
        axis.requested_state = AXIS_STATE_IDLE
        self.button_cancelloop.destroy()
        self.button_closeloop = Button(self.root,text = "pos cntrl",command = self.closeloop,width=15,bg="#DCDCDC")
        self.button_closeloop.place(x = 500,y = 150)
        self.setpos.destroy()
        self.button_setpos.destroy()

    def loop(self):
        self.lmain.after(10, self.loop)
        self.Tkinter_Current_status.set(str(round(axis.motor.current_control.Iq_setpoint,2)))
        self.Tkinter_POS_status.set(str(round(axis.encoder.pos_estimate,2)))

        
    def start(self):
        self.loop()
        self.root.mainloop()

    def on_closing(self):
        axis.requested_state = AXIS_STATE_IDLE
        self.root.destroy()
        exit()

x = gui()
def setpos():
    p = min(6,max(0,float(x.Tkinter_pos_setpoint.get())))
    axis.controller.input_pos = p
    time.sleep(0.5)
x.start()
