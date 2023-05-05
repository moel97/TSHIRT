from Functions._settings import *
from Functions.read_unoData import *
from Functions.Data_processing import *
##########################################################################################################START
def Dialog():
    def show_pg(frame):
        frame.tkraise()

    root =Tk()
    root.geometry('1000x1000')
    root.title('T.S.H.I.R.T')
    mainbigframe = Frame(root, bg='#333b3d')
    mainbigframe.pack(fill="both", expand=True)
    #####################################################################logo upper
    logosframe_upper = Frame(mainbigframe, borderwidth=5, bg='#025d6f')
    photo = Image.open("tuilm_logo.jpg")
    photo_rec = photo.resize((400, 100), Image.ANTIALIAS)
    u_conv_image = ImageTk.PhotoImage(photo_rec)
    labelu = Label(logosframe_upper, image=u_conv_image, bg='#025d6f')
    labelu.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
    photo2 = Image.open("tshirt_logo.jpg")
    photo_rec2 = photo2.resize((200, 200), Image.ANTIALIAS)
    u_conv_image2 = ImageTk.PhotoImage(photo_rec2)
    labelu2 = Label(logosframe_upper, image=u_conv_image2, bg='#025d6f')
    labelu2.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
    logosframe_upper.columnconfigure(0, weight=1)
    logosframe_upper.columnconfigure(1, weight=1)
    logosframe_upper.rowconfigure(0, weight=1)
    logosframe_upper.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

    ###########################################################################button frame
    button_frame = Frame(mainbigframe, borderwidth=5, bg='#333b3d')
    Patton_1 = Button(button_frame, text="Bewegungserfassung", font=(35), bg='#333b3d', fg="white",
                      command=lambda: show_pg(page1)).grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
    Patton_2 = Button(button_frame, text="Ergebnisse anzeigen", font=(35), bg='#FD841F',
                      command=lambda: show_pg(page2)).grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.rowconfigure(0, weight=1)
    button_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

    ################################################################################################mainframe
    mainframe = Frame(mainbigframe, borderwidth=5, bg='#333b3d')
    page1 = Frame(mainframe, border=4, bg='#333b3d')
    p_ports = Label(page1, text='Wähle eine Com Port aus', font=(25), borderwidth=5, bg='#333b3d', fg="white").grid(
        row=0, column=0, pady=10, padx=10, sticky="nsew")
    ports = import_comports()
    print("ports")
    print(ports)
    value_inside = StringVar(page1)
    value_inside.set("COM")
    drop = OptionMenu(page1, value_inside, *ports)
    drop.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
    e = tk.Entry(page1, width=90, borderwidth=5)
    e.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")
    value_inside2 = StringVar(page1)
    baud_rates = [9600, 14400, 19200, 38400, 57600, 115200]
    drop2 = OptionMenu(page1, value_inside2, *baud_rates)
    drop2.grid(row=1, column=1, pady=10, padx=10, sticky="nsew")
    p_rates = Label(page1, text='Wähle ein Baudrate aus', font=(25), borderwidth=5, bg='#333b3d', fg="white").grid(
        row=1, column=0, pady=10, padx=10, sticky="nsew")
    p2_label = Label(page1, text='Geben Sie den Dateinamen ein', font=(25), borderwidth=5, bg='#333b3d',
                     fg="white").grid(row=3, column=0, pady=10, padx=10, sticky="nsew")
    e2 = tk.Entry(page1, width=90, borderwidth=5)
    e2.grid(row=3, column=1, pady=10, padx=10, sticky="nsew")

    def open_path():
        path1 = filedialog.askdirectory()
        e.delete(0, END)
        e.insert(0, path1)

    Patton_Path1 = Button(page1, text='File Path', font=(25), command=lambda: open_path()).grid(row=2, column=0,
                                                                                                pady=10, padx=10,
                                                                                                sticky="nsew")
    Patton_start = Button(page1, text='START Program', font=(25),
                          command=lambda: Read_data(e.get() + "/" + e2.get(), value_inside.get(),
                                                    value_inside2.get())).grid(row=4, column=0, pady=10, padx=10,
                                                                               sticky="nsew")
    End_label = Label(page1, text='Drücken Sie lange die Taste "q", um das Programm zur Bewegungserfassung zu stoppen.',
                      font=(25), borderwidth=5, bg='#333b3d', fg="white").grid(row=4, column=1, pady=10, padx=10,
                                                                               sticky="nsew")
    page1.columnconfigure(0, weight=1)
    page1.columnconfigure(1, weight=1)

    page1.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
    ###########################################################################################Page2
    page2 = Frame(mainframe, border=4, bg='#FD841F')
    e2_p2 = tk.Entry(page2, width=90, borderwidth=5)
    e2_p2.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
    Patton_Path2 = Button(page2, text='File Path', font=(25), command=lambda: open_path2()).grid(row=0, column=0,
                                                                                                 pady=10, padx=10,
                                                                                                 sticky="nsew")

    def open_path2():
        path2 = filedialog.askopenfilename()
        e2_p2.delete(0, END)
        e2_p2.insert(0, path2)

    Patton_start2 = Button(page2, text='Graphen erstellen', font=(25), command=lambda: date_cleaning(e2_p2.get())).grid(
        row=1, column=0, pady=10, padx=10, sticky="nsew")

    page2.columnconfigure(0, weight=1)
    page2.columnconfigure(1, weight=1)
    page2.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
    ######################################################################################################
    mainframe.columnconfigure(0, weight=1)
    mainframe.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
    ###################################################################################################logos

    logosframe = Frame(mainbigframe, borderwidth=5, bg='#333b3d')
    photo = Image.open("logos.jpg")
    photo_recise = photo.resize((700, 250), Image.ANTIALIAS)
    conv_image = ImageTk.PhotoImage(photo_recise)
    label = Label(logosframe, image=conv_image, bg='#025d6f')
    label.pack(fill="both", expand=True)
    logosframe.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

    ########################################################################
    mainbigframe.columnconfigure(0, weight=1)
    mainbigframe.rowconfigure(0, weight=1)
    mainbigframe.rowconfigure(1, weight=1)
    mainbigframe.rowconfigure(2, weight=2)
    mainbigframe.rowconfigure(3, weight=5)
    root.iconbitmap('Logo_Cosima_cut.ICO')
    root.mainloop()
