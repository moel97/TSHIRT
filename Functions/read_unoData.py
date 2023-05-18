from Functions._settings import *
#reads data from Arduino's serial Port the function will stop if the user pressed Q from keyboard
#takes (string pasth to save the data in , the port number where the Arduino is saved, the baud rate of the Arduino)
def Read_data(xp_path,num_com,baud_rate):
    try:
        f = open(xp_path,"w")
        arduino = serial.Serial(num_com,115200)
        arr_raw_data = []
        bauddd= "AT+BAUD8"
        arduino.write(bauddd.encode())
        try:
            messagebox.showinfo("Info", "Datenerfassung wurde gestartet")
            while True:
                while(arduino.inWaiting()==0):
                    pass
                arduino_data = arduino.readline().decode()
                arr_raw_data.append(arduino_data)
                f.write(arduino_data)
                print(arduino_data)
                if keyboard.is_pressed("esc"):
                    messagebox.showinfo("Info", "Datenerfassung wurde gestoppt")
                    break
        except KeyboardInterrupt:
            pass



    except:
            messagebox.showinfo("ERROR","Falsche Dateneingabe")

##################################################################################################################

#inables the running of this module as a parallel process
def read_data_paralell(xp_path,num_com,baud_rate):
    Proc =multiprocessing.Process(target=Read_data,args= [xp_path,num_com,baud_rate])
    Proc.start()