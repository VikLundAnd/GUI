import tkinter as tk, threading
from tkinter import messagebox
import functools
import subprocess
import string
import serial.tools.list_ports
import serial
from tkinter import *
import time
import os
import imageio
from PIL import Image, ImageTk
import playsound
import datetime


class WakeupApplication():
    def __init__(self,master):
        #Define memory
        self.Rooms = []
        self.Units = []
        self.WakeUpRoutines = []
        self.readConfig()
        self.readWakeup()

        #Define all frames
        self.Frame = tk.Frame(master)
        self.select_transmitterFrame = tk.Frame()
        self.lockFrame = tk.Frame()
        self.mainFrame = tk.Frame()
        self.configFrame = tk.Frame()
        self.setupFrame = tk.Frame()
        self.add_roomFrame = tk.Frame()
        self.add_unitFrame = tk.Frame()
        self.select_roomFrame = tk.Frame()
        self.unit_connect_adressFrame = tk.Frame()
        self.select_wakeupFrame = tk.Frame()
        self.select_routineroomFrame = tk.Frame()
        self.deleteFrame = tk.Frame()
        self.delete_room_and_unitsFrame = tk.Frame()
        self.select_routineUnitFrame = tk.Frame()
        self.select_routineTimeFrame = tk.Frame()
        self.flashFrame = tk.Frame()
        self.select_routineDeactTimeFrame = tk.Frame()
        self.delete_room_and_units_extendedFrame = tk.Frame()
        self.delete_wakeupFrame = tk.Frame()


        self.correctPass = "a"
        self.video1_name = "test.avi"
        self.video1 = imageio.get_reader(self.video1_name)
        self.video2_name = "test 2.avi"
        self.video2 = imageio.get_reader(self.video2_name)
        self.HeaderImage = tk.PhotoImage(file = "Logo.gif")
        self.HeaderExists = False
        self.IntroRun = True
        self.Arduino = serial.Serial(baudrate=9600, stopbits=1)
        self.CodeReceived = ""

        self.TempWakeUpRoutines = []


        self.Frame.pack()
        self.select_transmitter_frame()


    def select_transmitter_frame(self):
        self.clearFrame()

        self.select_transmitterFrame = tk.Frame()
        self.select_transmitterFrame.pack()


        #Key press functions for flashFrame:
        def port_pressed(port):
            print(str(port[0])[3:])
            self.Arduino.port = str(port[0])
            self.Arduino.open()
            self.lock_frame()

        #Layout for deleteFrame:
        if (tuple(serial.tools.list_ports.comports()) != ()):
            Port_list = serial.tools.list_ports.comports()
            for port in Port_list:
                self.port_buttons = tk.Button(self.select_transmitterFrame, background = "#6c849c", anchor = tk.W , text=list(port[0]), command=functools.partial(port_pressed,port))
                self.port_buttons.pack(side = tk.TOP,fill = tk.X)
        else:
            #self.No_ports_messagebox = tk.messagebox.askretrycancel(title = "Ingen tilgængelige porte", message="Ingen tilgængelige porte.\nForbind enhed og forsøg igen.")
            #if self.No_ports_messagebox:
            #    self.select_transmitter_frame()
            #else:
            #    root.destroy()
            self.main_frame()


    def lock_frame(self):
        self.clearFrame()

        self.lockFrame = tk.Frame()
        self.lockFrame.pack()


        def stream_video(label):
            for image in self.video1.iter_data():
                try:
                    frame_image = ImageTk.PhotoImage(Image.fromarray(image))
                    label.config(image=frame_image)
                    label.image = frame_image
                except:
                    break

            while self.IntroRun:
                for image in self.video2.iter_data():
                    try:
                        frame_image = ImageTk.PhotoImage(Image.fromarray(image))
                        label.config(image=frame_image)
                        label.image = frame_image
                    except:
                        break
            return

        def code_check():
            while True:
                self.CodeReceived  = str(self.Arduino.read())[2]
                print("Code received : " + self.CodeReceived)
                if self.CodeReceived == 'u':
                    break

        def code_compare():
            while self.CodeReceived != 'u':
                #pass
                time.sleep(1)
            if (self.CodeReceived == 'u'):
                self.IntroRun = False
                self.main_frame()


        def enter_pressed():
            print("Du har trykket enter")
            self.IntroRun = False
            self.CodeReceived = 'u'



        videoFeed = tk.Label(self.lockFrame)
        videoFeed.pack()

        self.CodeIs = False

        self.video_thread = threading.Thread(target=stream_video, args=(videoFeed,))
        self.codechecker_thread = threading.Thread(target=code_check)
        self.codecompare_thread = threading.Thread(target=code_compare)
        self.enterpressed_thread = threading.Thread(target=enter_pressed)

        #root.bind('<Return>', self.enterpressed_thread.start())

        self.video_thread.start()
        self.codechecker_thread.start()
        self.codecompare_thread.start()




    def main_frame(self):
        self.clearFrame()


        if self.HeaderExists:
            pass
        else:
            header = tk.Label(root, image=self.HeaderImage, borderwidth =0, height = 70, background = "#1d2023")
            header.pack(side=tk.TOP);
            self.HeaderExists = True

        print("You are in the main menu:")
        self.mainFrame = tk.Frame()
        self.mainFrame.pack()

        #Key press functions for mainFrame:
        def Config_pressed():
            print("Config was pressed")
            self.config_frame()

        def settings_pressed():
            print("setup was pressed")
            self.setup_frame()

        def select_wakeup_pressed():
            self.select_wakeup_frame()


        def delete_pressed():
            self.delete_frame()


        #Layout for mainFrame:
        self.config_button = tk.Button(self.mainFrame, background = "#6c849c", anchor = tk.W , text="Konfigurér hus", command=Config_pressed)
        self.config_button.pack(side = tk.TOP,fill = tk.X)

        self.settings_button = tk.Button(self.mainFrame, background = "#6c849c", anchor = tk.W , text="Indstil morgenvækning", command=settings_pressed)
        self.settings_button.pack(side = tk.TOP,fill = tk.X)

        self.select_wakeup_button = tk.Button(self.mainFrame, background = "#b3e1af", anchor = tk.W , text="Vælg morgenvækning", command=select_wakeup_pressed)
        self.select_wakeup_button.pack(side = tk.TOP,fill = tk.X)

        self.delete_button = tk.Button(self.mainFrame, background = "#e1afaf", anchor = tk.W , text="Slet", command=delete_pressed)
        self.delete_button.pack(side = tk.TOP,fill = tk.X)


    def config_frame(self):
        self.clearFrame()

        self.configFrame = tk.Frame()
        self.configFrame.pack()

        #Key press functions for config_frame:
        def add_room_pressed():
            self.add_room_frame()

        def add_unit_pressed():
            self.select_room_frame()

        def to_main_pressed():
            self.main_frame()

        #Layout for configFrame:
        self.add_room_button = tk.Button(self.configFrame, background = "#6c849c", anchor = tk.W , text="Tilføj rum", command=add_room_pressed)
        self.add_room_button.pack(side = tk.TOP,fill = tk.X)

        self.add_unit_button = tk.Button(self.configFrame, background = "#6c849c", anchor = tk.W , text="Tilføj enhed", command=add_unit_pressed)
        self.add_unit_button.pack(side = tk.TOP,fill = tk.X)

        self.to_main_button = tk.Button(self.configFrame, background = "#6c849c", anchor = tk.W , text="[esc] Tilbage til main", command=to_main_pressed)
        self.to_main_button.pack(side = tk.TOP,fill = tk.X)
        root.bind('<Escape>', lambda noArg: to_main_pressed())

    def add_room_frame(self):
        self.clearFrame()

        self.add_roomFrame = tk.Frame()
        self.add_roomFrame.pack()

        def enter_pressed(event):
            if ((len(RoomName.get()) <= 20) and (len(self.Rooms) <= 16) and not(self.Rooms.count(RoomName.get()))):
                self.Rooms.append(RoomName.get())
                print(self.Rooms)
                self.save()
                self.config_frame()
            else:
                if (len(RoomName.get()) >= 20):
                    tk.messagebox.showinfo("Fejl!", "Navn overskrider 20 tegn.")
                if (len(self.Rooms) >= 16):
                    tk.messagebox.showinfo("Fejl!", "Der kan ikke være flere rum.")
                if (self.Rooms.count(RoomName.get())):
                    tk.messagebox.showinfo("Fejl!", "Rummet eksisterer allerede.")
                return

        def textbox_clicked(event):
            RoomName.set("")
            return

        #Layout for add_roomFrame:
        RoomName = tk.StringVar()
        RoomName.set("Rumnavn")
        self.enter_name = tk.Entry(self.add_roomFrame, textvariable = RoomName)
        self.enter_name.pack(side = tk.TOP,fill = tk.X)
        self.enter_name.bind("<Button-1>", textbox_clicked)

        root.bind('<Return>', enter_pressed)

    def select_room_frame(self):
        self.clearFrame()

        self.select_roomFrame = tk.Frame()
        self.select_roomFrame.pack()

        #Key press functions for config_frame:
        def select_room_pressed(room):
            self.selectedRoom = room
            self.add_unit_frame()
            pass

        #Layout for select_roomFrame:
        for room in self.Rooms:
            self.room_buttons = tk.Button(self.select_roomFrame, background = "#6c849c", anchor = tk.W , text=room, command=functools.partial(select_room_pressed,room))
            self.room_buttons.pack(side = tk.TOP,fill = tk.X)

    def add_unit_frame(self):
        self.clearFrame()

        print("You are in the add unit menu:")
        self.add_unitFrame = tk.Frame()
        self.add_unitFrame.pack()

        def enter_pressed(event):
            if ((len(UnitName.get()) <= 20) and (len(self.Units) <= 16) and not(self.Units.count(UnitName.get()))):
                self.selectedUnit = UnitName.get()
                #self.unit_connect_adress_frame("COM8")
                self.unit_connect_adress_frame()
            else:
                if (len(UnitName.get()) >= 20):
                    tk.messagebox.showinfo("Fejl!", "Navn overskrider 20 tegn.")
                if (len(self.Units) >= 16):
                    tk.messagebox.showinfo("Fejl!", "Der kan ikke være flere enheder.")
                if (self.Units.count(UnitName.get())):
                    tk.messagebox.showinfo("Fejl!", "Enheden eksisterer allerede.")
                return

        def textbox_clicked(event):
            UnitName.set("")
            return

        #Layout for add_unitFrame:
        UnitName = tk.StringVar()
        UnitName.set("Enhedsnavn")
        self.enter_name = tk.Entry(self.add_unitFrame,textvariable = UnitName)
        self.enter_name.pack(side = tk.TOP,fill = tk.X)
        self.enter_name.bind("<Button-1>", textbox_clicked)

        root.bind('<Return>', enter_pressed)



    def unit_connect_adress_frame(self):

        self.unit_connect_adressFrame = tk.Frame()
        self.unit_connect_adressFrame.pack()

        #Layout for enter_unit_adressFrame:
        count = 0

        def first_available_adress():
            Letter = ''
            Number = ""

            #LETTER CODE
            if [sublist[0] for sublist in self.Units].count(self.selectedRoom) > 0:
                for units in self.Units:

                    if units[0] == self.selectedRoom:
                        Letter = units[2][0]


            else:
                print("Liste: " + str([sublist[2][0] for sublist in self.Units]))

                for letter_ in reversed(range(ord('A'), ord('P') + 1)):

                    if [sublist[2][0] for sublist in self.Units].count(chr(letter_)) <= 0:
                        Letter = chr(letter_)


            if [sublist[2][0] for sublist in self.Units].count(Letter) > 0:
                tempList = []

                for units in self.Units:
                    tempList.append(units[2][1:])

                print(tempList)

                tempList.sort()

                for index, numbers in enumerate(tempList):
                    print(int(numbers))
                    print(index)
                    if index + 1 != int(numbers):
                        if index + 1 < 10:
                            Number = "0" + str(index + 1)
                        else:
                            Number = str(index + 1)
                    else:
                        if index + 1 < 10:
                            Number = "0" + str(index + 2)
                        else:
                            Number = str(index + 2)


            else:
                Number = "01"

            return Letter + Number


        def code_check():
            while True:
                self.CodeReceived  = str(self.Arduino.read())[2]
                print("Code received : " + self.CodeReceived)
                if self.CodeReceived == 'a':
                    break


        def code_compare():
            while self.CodeReceived != 'a':
                pass
                #time.sleep(1)
            if (self.CodeReceived == 'a'):
                self.IntroRun = False
                self.main_frame()


        infoLabel = tk.Label(self.unit_connect_adressFrame, text="Skifter adresse")
        infoLabel.pack(side = tk.TOP,fill = tk.X)

        Adress = first_available_adress()

        self.changeAdressRequest(Adress)

        self.codechecker_thread = threading.Thread(target=code_check)
        self.codecompare_thread = threading.Thread(target=code_compare)

        self.codechecker_thread.start()
        self.codecompare_thread.start()



        self.Units.append([self.selectedRoom, self.selectedUnit, Adress])
        self.save()

        #self.config_frame()


    def select_wakeup_frame(self):
        self.clearFrame()

        self.select_wakeupFrame = tk.Frame()
        self.select_wakeupFrame.pack()

        #Key press functions for select_wakeupFrame:
        def select_wakeup_pressed(idx):
            #self.selectedWakeup = wakeups
            self.save_flash(idx)
            self.flash_frame()



        #Layout for select_wakeupFrame:
        for idx, wakeups in enumerate(self.WakeUpRoutines):
            self.wakeup_buttons = tk.Button(self.select_wakeupFrame, background = "#6c849c", anchor = tk.W , text=wakeups[0], command=functools.partial(select_wakeup_pressed,idx))
            self.wakeup_buttons.pack(side = tk.TOP,fill = tk.X)

    def setup_frame(self):
        self.clearFrame()

        self.setupFrame = tk.Frame()
        self.setupFrame.pack()

        #Layout for setupFrame:
        def enter_pressed(event):
            if ((len(wakeupName.get()) <= 20) and (len(self.WakeUpRoutines) <= 16) and not(self.WakeUpRoutines.count(wakeupName.get()))):
                self.TempWakeUpRoutines.append([wakeupName.get()][0])
                print(self.WakeUpRoutines)
                self.select_routineroom_frame()
            else:
                if (len(wakeupName.get()) >= 20):
                    tk.messagebox.showinfo("Fejl!", "Navn overskrider 20 tegn.")
                if (len(self.WakeUpRoutines) >= 16):
                    tk.messagebox.showinfo("Fejl!", "Der kan ikke være flere rutiner.")
                if (self.WakeUpRoutines.count(wakeupName.get())):
                    tk.messagebox.showinfo("Fejl!", "Rutinen eksisterer allerede.")
                return

        def textbox_clicked(event):
            wakeupName.set("")
            return

        #Layout for setupFrame:
        wakeupName = tk.StringVar()
        wakeupName.set("Morgenvækningsrutine")
        self.enter_name = tk.Entry(self.setupFrame, textvariable = wakeupName)
        self.enter_name.pack(side = tk.TOP,fill = tk.X)
        self.enter_name.bind("<Button-1>", textbox_clicked)

        root.bind('<Return>', enter_pressed)

    def select_routineroom_frame(self):
        self.clearFrame()

        self.select_routineroomFrame = tk.Frame()
        self.select_routineroomFrame.pack()

        #Key press functions for select_routineroomFrame:
        def room_pressed(room):
            self.selectedRoutineRoom = room
            self.select_routineUnit_frame()

        #Layout for select_routineroomFrame:
        for room in self.Rooms:
            self.room_buttons = tk.Button(self.select_routineroomFrame, background = "#6c849c", anchor = tk.W , text=room, command=functools.partial(room_pressed,room))
            self.room_buttons.pack(side = tk.TOP,fill = tk.X)

    def select_routineUnit_frame(self):
        self.clearFrame()

        self.select_routineUnitFrame = tk.Frame()
        self.select_routineUnitFrame.pack()

        #Key press functions for select_routineroomFrame:
        def unit_pressed(unit):
            self.selectedRoutineUnit = unit[2]
            self.select_routineActTime_frame()

        def escape_pressed():
            if len(self.TempWakeUpRoutines) > 2:
                self.WakeUpRoutines.append([*self.TempWakeUpRoutines])

                self.TempWakeUpRoutines.clear()
                self.save_routine()
                self.main_frame()

        #Layout for select_routineroomFrame:
        for unit in self.Units:
            if unit[0] == self.selectedRoutineRoom:
                self.unit_buttons = tk.Button(self.select_routineUnitFrame, background = "#6c849c", anchor = tk.W , text=unit[1], command=functools.partial(unit_pressed,unit))
                self.unit_buttons.pack(side = tk.TOP,fill = tk.X)

        root.bind('<Escape>', lambda noArg: escape_pressed())

    def select_routineActTime_frame(self):
        self.clearFrame()

        self.select_routineTimeFrame = tk.Frame()
        self.select_routineTimeFrame.pack()

        #Key press functions for select_routineTimeFrame:
        def enter_pressed(event):
            if ((len(time.get()) == 5) and (time.get()[2] == ':') and (time.get()[0:1].isnumeric()) and (time.get()[3:4].isnumeric())):
                self.selectedRoutineActTime = [time.get()]
                self.select_routineDeactTime_frame()
            else:
                return

        def textbox_clicked(event):
            time.set("")
            return


        #Layout for enter_unit_adressFrame:
        time = tk.StringVar()
        time.set("HH:MM")
        self.enter_time = tk.Entry(self.select_routineTimeFrame,textvariable = time)
        self.enter_time.pack(side = tk.TOP,fill = tk.X)
        self.enter_time.bind("<Button-1>", textbox_clicked)

        root.bind('<Return>', enter_pressed)

    def select_routineDeactTime_frame(self):
        self.clearFrame()

        self.select_routineDeactTimeFrame = tk.Frame()
        self.select_routineDeactTimeFrame.pack()

        #Key press functions for select_routineTimeFrame:
        def enter_pressed(event):
            if ((len(time.get()) == 5) and (time.get()[2] == ':') and (time.get()[0:1].isnumeric()) and (time.get()[3:4].isnumeric())):
                self.selectedRoutineDeactTime = [time.get()]

                self.TempWakeUpRoutines.append(self.selectedRoutineActTime[0])
                self.TempWakeUpRoutines.append(self.selectedRoutineUnit)
                self.TempWakeUpRoutines.append(self.selectedRoutineDeactTime[0])

                self.select_routineroom_frame()
            else:
                return

        def textbox_clicked(event):
            time.set("")
            return



        #Layout for enter_unit_adressFrame:
        time = tk.StringVar()
        time.set("HH:MM")
        self.enter_time = tk.Entry(self.select_routineDeactTimeFrame,textvariable = time)
        self.enter_time.pack(side = tk.TOP,fill = tk.X)
        self.enter_time.bind("<Button-1>", textbox_clicked)

        root.bind('<Return>', enter_pressed)

    def delete_frame(self):
        self.clearFrame()

        self.deleteFrame = tk.Frame()
        self.deleteFrame.pack()

        #Key press functions for delete_frame:
        def delete_room_and_units_pressed():
            self.delete_room_and_units_frame()

        def delete_routine_pressed():
            self.delete_wakeup_frame()


        #Layout for deleteFrame:
        self.delete_room_and_units_button = tk.Button(self.deleteFrame, background = "#6c849c", anchor = tk.W , text="Vælg rum for at slette enhed eller rum", command=delete_room_and_units_pressed)
        self.delete_room_and_units_button.pack(side = tk.TOP,fill = tk.X)

        self.delete_routine_button = tk.Button(self.deleteFrame, background = "#6c849c", anchor = tk.W , text="Slet morgenvækningsprogram", command=delete_routine_pressed)
        self.delete_routine_button.pack(side = tk.TOP,fill = tk.X)

    def delete_room_and_units_frame(self):
        self.clearFrame()

        self.delete_room_and_unitsFrame = tk.Frame()
        self.delete_room_and_unitsFrame.pack()

        #Key press functions for delete_room_and_units_frame:
        def room_pressed(room):
            self.delete_room_and_units_frame_extended(room)

        def to_main_pressed():
            self.main_frame()

        #Layout for delete_room_and_units_frame:
        for room in self.Rooms:
            self.room_buttons = tk.Button(self.delete_room_and_unitsFrame, background = "#6c849c", anchor = tk.W , text=room, command=functools.partial(room_pressed,room))
            self.room_buttons.pack(side = tk.TOP,fill = tk.X)


        self.to_main_button = tk.Button(self.delete_room_and_unitsFrame, background = "#6c849c", anchor = tk.W , text="Tilbage til main", command=to_main_pressed)
        self.to_main_button.pack(side = tk.TOP,fill = tk.X)
        root.bind('<Escape>', lambda noArg: to_main_pressed())


    def delete_room_and_units_frame_extended(self, room):
        self.clearFrame()

        self.delete_room_and_units_extendedFrame = tk.Frame()
        self.delete_room_and_units_extendedFrame.pack()

        #Key press functions for delete_room_and_units_frame:
        def delete_room_pressed():
            self.delete_room(room)
            self.delete_room_and_units_frame()

        def unit_pressed(unit):
            self.delete_unit(unit)
            self.delete_room_and_units_frame_extended(room)

        def to_main_pressed():
            self.main_frame()

        #Layout for delete_room_and_units_frame:
        for unit in self.Units:
            if unit[0] == room:
                self.room_unit_buttons = tk.Button(self.delete_room_and_units_extendedFrame, background = "#6c849c", anchor = tk.W , text=unit[1], command=functools.partial(unit_pressed,unit))
                self.room_unit_buttons.pack(side = tk.TOP,fill = tk.X)

        self.delete_room_button = tk.Button(self.delete_room_and_units_extendedFrame, background = "#6c849c", anchor = tk.W , text="Slet rum", command=delete_room_pressed)
        self.delete_room_button.pack(side = tk.TOP,fill = tk.X)

        self.to_main_button = tk.Button(self.delete_room_and_units_extendedFrame, background = "#6c849c", anchor = tk.W , text="Tilbage til main", command=to_main_pressed)
        self.to_main_button.pack(side = tk.TOP,fill = tk.X)

        root.bind('<Escape>', lambda noArg: to_main_pressed())


    def flash_frame(self):
        self.clearFrame()

        self.flashFrame = tk.Frame()
        self.flashFrame.pack()

        self.flash()
        self.main_frame()

    def delete_wakeup_frame(self):

        self.clearFrame()

        self.delete_wakeupFrame = tk.Frame()
        self.delete_wakeupFrame.pack()

        #Key press functions for select_wakeupFrame:
        def wakeup_pressed(wakeups):
            self.delete_wakeup(wakeups)
            self.delete_wakeup_frame()

        def to_main_pressed():
            self.main_frame()


        #Layout for select_wakeupFrame:
        for wakeups in self.WakeUpRoutines:
            self.wakeup_buttons = tk.Button(self.delete_wakeupFrame, background = "#6c849c", anchor = tk.W , text=wakeups[0], command=functools.partial(wakeup_pressed,wakeups))
            self.wakeup_buttons.pack(side = tk.TOP,fill = tk.X)

        root.bind('<Escape>', lambda noArg: to_main_pressed())






    #Define functions
    def clearFrame(self):
        #Clear frames
        self.select_transmitterFrame.destroy()
        self.lockFrame.destroy()
        self.mainFrame.destroy()
        self.configFrame.forget()
        self.setupFrame.forget()
        self.add_roomFrame.forget()
        self.add_unitFrame.forget()
        self.select_roomFrame.forget()
        self.unit_connect_adressFrame.forget()
        self.select_wakeupFrame.forget()
        self.select_routineroomFrame.forget()
        self.deleteFrame.forget()
        self.delete_room_and_unitsFrame.forget()
        self.select_routineUnitFrame.forget()
        self.select_routineTimeFrame.forget()
        self.flashFrame.forget()
        self.select_routineDeactTimeFrame.forget()
        self.delete_room_and_units_extendedFrame.forget()
        self.delete_wakeupFrame.forget()



    def readConfig(self):

        #Read and parse config.txt
        config = open("config.txt",'r+')

        RoomText = config.readline()
        RoomText = RoomText.split('\n')[0]
        try:
            RoomText = RoomText.split(':')[1]
            Room = RoomText[1:-1].split(',')

            for elements1 in Room:
                if len(elements1) > 3:
                    self.Rooms.append(elements1[2:-1])
        except:
            pass


        UnitsText = config.readline()

        try:
            UnitsText = UnitsText.split(':')[1][1:-2]
            #print(UnitsText)
            #UnitsText = UnitsText[1:-1]
            #print(UnitsText)

            Unit = UnitsText.split('],')
            #print(Unit)


            for elements1 in Unit:


                UnitGroup = elements1[3:-1].split(',')

                self.Units.append([UnitGroup[0][0:-1],UnitGroup[1][2:-1], UnitGroup[2][2:]])
        except:
            pass

    def readWakeup(self):

        config = open("wakeup.txt",'r+')

        configFile = config.readlines()


        for line in configFile:

            #If is a wakeupname
            if line[0] == '\"':
                #print(line[1:-2])
                RoutineArray = []
                RoutineArray.append(line[1:-2])


            #If is a wakeupname
            if line[0] == '[':
                routineCollections = line[1:-3].split('],')



                for Collection in routineCollections:
                    RoutineAttr = Collection[:].split(',')
                    #print(RoutineAttr)

                    for attributes in RoutineAttr:
                        #print(attributes[2:-1])
                        RoutineArray.append(attributes[2:-1])


                self.WakeUpRoutines.append(RoutineArray)





    def save(self):
        file = open("config.txt", mode="w+")
        #print("Rooms: " + str(self.Rooms[0:len(self.Rooms)]) + "\nUnits: " + str(self.Units[0:len(self.Units)]))
        file.write("Rooms: " + str(self.Rooms[0:len(self.Rooms)]) + "\nUnits: " + str(self.Units[0:len(self.Units)]))

    def save_routine(self):
        file = open("wakeup.txt", mode="w+")

        for WakeUpRoutines in self.WakeUpRoutines:
            for idx, wakeupAttributes in enumerate(WakeUpRoutines):

                if idx == 0:
                    file.write("\"" + wakeupAttributes + "\"\n[")
                elif idx % 3 == 1: # Is activation
                    if idx > 3:
                        file.write(',')
                    file.write("[\'" + wakeupAttributes + "\',")

                elif idx % 3 == 2: # Is adress
                    file.write(" \'" + wakeupAttributes + "\',")

                elif idx % 3 == 0: # Is deactivation
                    file.write(" \'" + wakeupAttributes + "\']")


            file.write("]\n")


    def save_flash(self, idx):
        file = open("flash.txt", mode="w+")

        file.write("[")
        for index, attribute in enumerate(self.WakeUpRoutines[idx][1:]):
            if index % 3 == 0: # Is activation
                if idx > 3:
                    file.write(',')
                file.write("[\'" + attribute + "\',")

            elif index % 3 == 1: # Is adress
                file.write(" \'" + attribute + "\',")

            elif index % 3 == 2: # Is deactivation
                if index < (len(self.WakeUpRoutines[idx]) - 3):
                    file.write(" \'" + attribute + "\'], ")
                else:
                    file.write(" \'" + attribute + "\']")

        file.write("]")

        #file.write(" (" + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ")")
        file.write(" (" + str(datetime.datetime.now())[11:-10] +")")


    def delete_room(self,room):
        self.Rooms.remove(room)

        indexes = []

        for idx, units in enumerate(self.Units):
            print(units[0] + "is" + room)
            if units[0] == room:
                indexes.append(idx)

        for idx in reversed(indexes):
            self.Units.pop(idx)


        self.save()
        return

    def delete_unit(self,unit):
        #Remove unit
        for idx, units in enumerate(self.Units):
            if units[2] == unit[2]:
                self.Units.pop(idx)

        #Remove associated WakeUpRoutines
        for routines in self.WakeUpRoutines:

            for index, attributes in enumerate(routines):

                if index % 3 == 2: #If is an adress
                    if attributes == unit[2]:
                        print(self.WakeUpRoutines[int(( index / 3 ) - 1)])
                        del self.WakeUpRoutines[int(( index / 3 ) - 1)]


        self.save()
        self.save_routine()
        return

    def delete_wakeup(self, wakeups):
        self.WakeUpRoutines.remove(wakeups)
        self.save_routine()

    def flash(self):
        file = open("flash.txt", mode="r")
        lines = file.read()
        print("p" + lines + "\r")

        self.Arduino.write("p".encode('ascii') + lines.encode('ascii') + "\r".encode('ascii'))

        #subprocess.call(['SerialFlasher.exe', str(port[0])[3:]])


    def changeAdressRequest(self, adress):
        self.Arduino.write("rP16".encode('ascii') + adress.encode('ascii') + "\r".encode('ascii'))
        #subprocess.call(['AdressRequest.exe', str(port[0])[3:], "P16", adress])




root = tk.Tk()
root.configure(background="#1d2023")

#photo = tk.PhotoImage(file = "Logo.gif")
#header = tk.Label(root,image=photo, borderwidth =0, height = 70, background = "#1d2023")
#header.pack(side=tk.TOP);

root.resizable(0,0)
root.geometry("900x600+300+100")

App = WakeupApplication(root)
root.mainloop()
